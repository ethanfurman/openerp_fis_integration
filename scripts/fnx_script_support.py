"""
support for short-running scripts
"""

__all__ = [
        'Notify', 'send_mail', 'grouped', 'grouped_by_column',
        'zip_longest',
        'NOW', 'TOMORROW',
        ]

try:
    from itertools import izip_longest as zip_longest
except ImportError:
    from itertools import zip_longest

from antipathy import Path
from datetime import timedelta
from dbf import DateTime
from scription import Exit, error, Job, OrmFile
import time

NOW = DateTime.now()
TOMORROW = NOW.replace(delta_day=+1).date()

BASE = Path('/home/openerp/sandbox')
SCHEDULE = BASE / 'etc/notify.ini'
NOTIFIED = BASE / 'var/notified.'

SCRIPT_NAME = None

class Notify(object):

    def __init__(self, name, schedule=SCHEDULE, notified=NOTIFIED, cut_off=0):
        # name: name of script (used for notified file name)
        # schedule: file that holds user name, email, text, and availability
        # notified: file that rememebers who has been notified
        # cut_off: how long to wait, in minutes, before resending errors or
        # sending all clear
        self.name = name
        self.schedule = Path(schedule)
        notified = Path(notified)
        if notified == NOTIFIED:
            notified += name
        self.notified = notified
        self.cut_off = timedelta(seconds=cut_off * 60)

    def __call__(self, errors):
        """
        send errors to valid recipients or cancellation to all notified thus far

        notification file format
        ---
        time contacted      address
        2020-05-20 03:47    ethan@stoneleaf.us
        ---
        """
        # script_name: name of calling script (used in subject line)
        # schedule: file with schedules of whom to contact and when
        # notified: file with contacted details
        # errors: list of errors (will become the message body)
        # cut_off: how long before an error free condition clears the last error
        #          how long since the last error before a new error is reported
        if not errors:
            if not self.notified.exists():
                return Exit.Success
            last_accessed = self.notified.stat().st_atime
            if NOW - DateTime.fromtimestamp(last_accessed) < self.cut_off:
                # too soon to notify, maybe next time
                return Exit.Success
            # get names from file and notify each one that problem is resolved
            addresses = self.get_notified()
            subject = "%s: all good" % self.name
            message = "problem has been resolved"
        else:
            # errors happened; check if notified needs (re)creating
            create_error_file = False
            if not self.notified.exists():
                create_error_file = True
            else:
                last_accessed = self.notified.stat().st_atime
                if NOW - DateTime.fromtimestamp(last_accessed) > self.cut_off:
                    # file should have been deleted; create fresh now
                    create_error_file = True
            if create_error_file:
                with open(self.notified, 'w') as fh:
                    fh.write("time contacted      address\n")
            self.notified.touch((time_stamp(NOW), None))
            all_addresses = self.get_recipients()
            addresses = self.filter_recipients(all_addresses)
            subject = "%s: errors encountered" % self.name
            message = ''.join(errors)
        sent_addresses, failed_to_send = send_mail(addresses, subject, message)
        if failed_to_send:
            error('\n\nUnable to contact:\n  %s' % ('\n  '.join(failed_to_send)))
        if errors:
            self.update_recipients(sent_addresses)
        else:
            self.notified.unlink()
        if errors or failed_to_send:
            return Exit.UnknownError
        else:
            return Exit.Success

    def filter_recipients(self, addresses):
        """
        return recipients that have not been contacted for current situation
        """
        with open(self.notified) as fh:
            lines = [line for line in fh.read().strip().split('\n') if line]
        if lines and lines[0].startswith('time'):
            lines.pop(0)
        contacted = []
        for line in lines:
            date, time, address = line.split()
            contacted.append(address)
        return [a for a in addresses if a not in contacted]

    def get_notified(self):
        """
        return address that have been notified

        file format is
        ---
        time contacted      address
        2020-05-20 03:47    ethan@stoneleaf.us
        ---
        """
        addresses = []
        with open(self.notified) as fh:
            data = fh.read().strip()
        if data:
            addresses = [line.split()[2] for line in data.split('\n')]
        return addresses

    def get_recipients(self):
        """
        read address file and return eligible recipients based on allowed times

        recipient file format is scription's OrmFile
        ---
        users = ['ethan', 'emile']
        email = None
        text = None

        [ethan]
        email = ['ethan@stoneleaf.us', ]
        text =  ['9715061961@vtext.com', ]

        [emile]
        email = ['emile@gmail.com', ]
        text = ['6503433458@tmomail.net', ]

        [available]
        ethan = ('Mo-Fr:600-1900', 'Su:1700-2100')
        emile = True
        tony = True
        ron = True

        [available.process_openerp_orders]
        ---
        """
        addresses = []
        settings = OrmFile(self.schedule)
        if self.name not in settings.available:
            raise ValueError('%r not in %s' % (self.name, SCHEDULE))
        section = settings.available[self.name]
        for user in settings.users:
            email = settings[user].email
            text = settings[user].text
            times = section[user]
            if times is True:
                available = WeeklyAvailability.always()
            elif times:
                available = WeeklyAvailability(*section[user])
            else:
                available = WeeklyAvailability.none()
            if email:
                addresses.extend(email)
            if text and NOW in available:
                addresses.extend(text)
        return addresses


    def update_recipients(self, addresses):
        """
        update notification file with who was contacted at what time
        """
        with open(self.notified, 'a') as fh:
            for address in addresses:
                fh.write('%-20s %s\n' % (NOW.strftime('%Y-%m-%d %H:%M'), address))


def send_mail(recipients, subject, message):
    """
    use system mail command to send MESSAGE to RECIPIENTS
    """
    sent_addresses = []
    failed_to_send = []
    for address in recipients:
        # may be skipped if all eligible addresses have already been notified
        try:
            job = Job(
                    '/usr/bin/mail -# -s "%s" %s' % (subject, address),
                    pty=True,
                    )
            job.communicate(input=message+'\n\x04', timeout=300)
            sent_addresses.append(address)
        except Exception as exc:
            error(exc)
            failed_to_send.append(address)
            continue
    return sent_addresses, failed_to_send

class WeeklyAvailability(object):
    """
    maintain periods of availability on a weekly basis
    """
    def __init__(self, *times):
        # times -> ['Mo:800-1700', 'Tu,Th:1100-1330,1730-2000', 'We:-', 'Fr', 'Sa-Su:1400-2100']
        self.text = str(times)
        matrix = {
                'mo': [0] * 1440,
                'tu': [0] * 1440,
                'we': [0] * 1440,
                'th': [0] * 1440,
                'fr': [0] * 1440,
                'sa': [0] * 1440,
                'su': [0] * 1440,
                }
        for period in times:
            period = period.lower()
            if ':' not in period:
                period += ':'
            days, minutes = period.split(':')
            if minutes == '-':
                minutes = None
            elif minutes == '':
                minutes = ['0-2359']
            else:
                minutes = minutes.split(',')
            for day in which_days(days):
                day = matrix[day]
                if minutes is None:
                    continue
                for sub_period in minutes:
                    start, end = sub_period.split('-')
                    start = int(start[:-2] or 0) * 60 + int(start[-2:])
                    end = int(end[:-2] or 0) * 60 + int(end[-2:])
                    for minute in range(start, end+1):
                        day[minute] = 1
        self.days = [matrix['su'], matrix['mo'], matrix['tu'], matrix['we'], matrix['th'], matrix['fr'], matrix['sa'], matrix['su']]

    def __repr__(self):
        return "WeeklyAvailability(%r)" % self.text

    def __contains__(self, dt):
        """
        checks if dt.day, hour, minute is 1
        """
        day = dt.isoweekday()
        moment = dt.hour * 60 + dt.minute
        return self.days[day][moment] == 1

    @classmethod
    def always(cls):
        """
        create a WeeklyAvailability with all availability
        """
        return cls('su-sa')

    @classmethod
    def none(cls):
        """
        create a WeeklyAvailability with no availability
        """
        return cls('su-sa:-')


def which_days(text):
    week = ['su','mo','tu','we','th','fr','sa']
    text = text.lower()
    groups = text.split(',')
    days = []
    for group in groups:
        if '-' not in group:
            days.append(group)
        else:
            start, stop = group.split('-')
            if start not in week:
                raise ValueError('invalid start day: %r' % (start, ))
            if stop not in week:
                raise ValueError('invalid stop day: %r' % (stop, ))
            start = week.index(start)
            while True:
                days.append(week[start])
                if week[start] == stop:
                    break
                start = (start + 1) % 7
    return days

def time_stamp(dt):
    "return POSIX timestamp as float"
    return time.mktime((dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, -1, -1, -1)) + dt.microsecond / 1e6

def grouped(it, size):
    'yield chunks of it in groups of size'
    if size < 1:
        raise ValueError('size must be greater than 0 (not %r)' % size)
    result = []
    count = 0
    for ele in it:
        result.append(ele)
        count += 1
        if count == size:
            yield tuple(result)
            count = 0
            result = []
    if result:
        yield tuple(result)

def grouped_by_column(it, size):
    'yield chunks of it in groups of size columns'
    if size < 1:
        raise ValueError('size must be greater than 0 (not %r)' % size)
    elements = list(it)
    iters = []
    rows, remainder = divmod(len(elements), size)
    if remainder:
        rows += 1
    for column in grouped(elements, rows):
        iters.append(column)
    while len(iters) < size:
        iters.append(iter(' '))
    return zip_longest(*iters, fillvalue='')
