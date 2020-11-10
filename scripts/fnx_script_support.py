"""
support for short-running scripts
"""

__all__ = [
        'notify', 'send_mail', 'grouped', 'grouped_by_column',
        'zip_longest',
        'NOW', 'TOMORROW', 'SCHEDULE', 'NOTIFIED',
        ]

try:
    from itertools import izip_longest as zip_longest
except ImportError:
    from itertools import zip_longest

from aenum import Enum
from dbf import DateTime
from scription import Exit, error, Job 
import time

NOW = DateTime.now()
TOMORROW = NOW.replace(delta_day=+1).date()

class FileType(Enum):
    SCHEDULE = "addresses and times"
    NOTIFIED = "who's been contacted"
SCHEDULE, NOTIFIED = FileType.SCHEDULE, FileType.NOTIFIED

def filter_recipients(addresses, notified_file):
    """
    return recipients that have not been contacted for current situation
    """
    with open(notified_file) as fh:
        lines = [line for line in fh.read().strip().split('\n') if line]
    if lines and lines[0].startswith('time'):
        lines.pop(0)
    contacted = []
    for line in lines:
        date, time, address = line.split()
        contacted.append(address)
    return [a for a in addresses if a not in contacted]

def get_recipients(source_file, source_type):
    """
    read address file and return eligible recipients based on allowed times
    """
    if source_type is NOTIFIED:
        with open(source_file) as fh:
            addresses = [line.split()[2] for line in fh.read().strip().split('\n')]
    elif source_type is SCHEDULE:
        with open(source_file) as fh:
            lines = [line for line in fh.read().strip().split('\n') if line]
        if lines and lines[0].startswith('email'):
            lines.pop(0)
        addresses = []
        for line in lines:
            pieces = line.split()
            if len(pieces) == 1:
                # email only
                email, = pieces
                phone = None
                availability = WeeklyAvailability.none()
            elif len(pieces) == 2:
                # email and phone (means always available)
                email, phone = pieces
                availability = WeeklyAvailability.always()
            else:
                email, phone = pieces[:2]
                availability = WeeklyAvailability(*pieces[2:])
            #
            addresses.append(email)
            if phone and NOW in availability:
                addresses.append(phone)
    else:
        raise ValueError('unknown source type: %r' % (source_type, ))
    return addresses


def notify(script_name, schedule, notified, errors, cut_off):
    """
    send errors to valid recipients or cancellation to all notified thus far
    """
    # script_name: name of calling script (used in subject line)
    # schedule: file with schedules of whom to contact and when
    # notified: file with contacted details
    # errors: list of errors (will become the message body)
    # cut_off: how long before an error free condition clears the last error
    #          how long since the last error before a new error is reported
    if not errors:
        if not notified.exists():
            return Exit.Success
        last_accessed = notified.stat().st_atime
        if NOW - DateTime.fromtimestamp(last_accessed) < cut_off:
            # too soon to notify, maybe next time
            return Exit.Success
        # get names from file and notify each one that problem is resolved
        addresses = get_recipients(notified, source_type=NOTIFIED)
        subject = "%s: all good" % script_name
        message = "problem has been resolved"
    else:
        # errors happened; check if notified needs (re)creating
        create_error_file = False
        if not notified.exists():
            create_error_file = True
        else:
            last_accessed = notified.stat().st_atime
            if NOW - DateTime.fromtimestamp(last_accessed) > cut_off:
                # file should have been deleted; create fresh now
                create_error_file = True
        if create_error_file:
            with open(notified, 'w') as fh:
                fh.write("time contacted      address\n")
        notified.touch((time_stamp(NOW), None))
        all_addresses = get_recipients(schedule, source_type=SCHEDULE)
        addresses = filter_recipients(all_addresses, notified)
        subject = "%s: errors encountered" % script_name
        message = ''.join(errors)
    sent_addresses, failed_to_send = send_mail(addresses, subject, message)
    if failed_to_send:
        error('\n\nUnable to contact:\n  %s' % ('\n  '.join(failed_to_send)))
    if errors:
        update_recipients(sent_addresses, notified)
    else:
        notified.unlink()
    if errors or failed_to_send:
        return Exit.UnknownError
    else:
        return Exit.Success

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

def update_recipients(addresses, notified):
    """
    update notification file with who was contacted at what time
    """
    with open(notified, 'a') as fh:
        for address in addresses:
            fh.write('%-20s %s\n' % (NOW.strftime('%Y-%m-%d %H:%M'), address))


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
    return zip_longest(*iters, fillvalue='')

