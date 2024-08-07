#!/usr/local/bin/suid-python --virtualenv
"""
transform the order output from OpenERP's Customer Portal Online Ordering
to a transfer file that FIS can import
"""
from __future__ import print_function

from scription import *
from fnx_script_support import *
from antipathy import Path
from traceback import format_exception_only
from dbf import Date, Period
import re
import sys

# all order numbers must be in the 10000-19999 range or we have collisions
# with other FIS-feeding processes

BASE_SEQ = 10000
CUT_OFF = 10

EOE_PATH = Path("/mnt/11-111/home/eoe/")
BASE_PATH = Path("/home/openerp/sandbox/openerp/var/fis_integration/orders")
ORDERS = BASE_PATH
ARCHIVE = BASE_PATH / "archive"
RECIPIENT_FILE = BASE_PATH / 'notify'
ERROR_FILE = BASE_PATH / 'notified'

## API

@Command(
        )
def process_openerp_orders():
    """
    transform OpenERP Customer Portal orders into FIS input
    """
    # default ship date
    # order files to process
    new_order_list = get_files_to_process(ORDERS)
    errors = []
    if new_order_list:
        if not EOE_PATH.exists():
            msg = "directory does not exist: '%s\n%d order(s) pending'" % (EOE_PATH, len(new_order_list))
            error(msg)
            errors.append(msg)
        else:
            for order_file in new_order_list:
                process(order_file, errors)
    notify = Notify(script_name)
    return notify(errors)


@Command(
        date=Spec('process orders submitted on DATE', OPTION, type=Date),
        order_no=Spec('specific order no', OPTION),
        transmitter_line=Spec('complete first line of file if order_no is for a non-HEB customer', OPTION),
        )
def resubmit(date, order_no, transmitter_line):
    if transmitter_line and not order_no:
        abort('must specify ORDER-NO if TRANSMITTER-NO given')
    target_period = None
    if date:
        target_period = Period(date.year, date.month, date.day)
    archive_order_list = get_files_to_process(ARCHIVE, target_period)
    count = 0
    for order in archive_order_list:
        if order_no and order_no != order.stem:
            continue
        with open(order) as in_file:
            data = in_file.read().strip().split('\n')
        first_line = data[0]
        if not first_line.endswith('-False'):
            continue
        if heb(first_line):
            tx_id = '150' + heb.groups()[0]
            data[0] = first_line[:6] + tx_id
            bk_arc = order.strip_ext() + '.bak'
            tmp_submit = ORDERS / order.stem
            final_submit = tmp_submit + '.txt'
            print()
            print('source file: %s' % order)
            print('backup file: %s' % bk_arc)
            print('submit file: %s' % tmp_submit)
            print('submit file: %s' % final_submit)
            print('contents:\n%s' % '\n'.join(data))
            print('\n')
            with open(tmp_submit, 'w') as out_file:
                out_file.write('\n'.join(data))
            order.rename(bk_arc)
            tmp_submit.rename(final_submit)
            count += 1
        else:
            if not transmitter_line:
                error('TRANSMITTER-NO must be specified for non-HEB customers')
            data[0] = transmitter_line
            bk_arc = order.strip_ext() + '.bak'
            tmp_submit = ORDERS / order.stem
            final_submit = tmp_submit + '.txt'
            print()
            print('source file: %s' % order)
            print('backup file: %s' % bk_arc)
            print('submit file: %s' % tmp_submit)
            print('submit file: %s' % final_submit)
            print('contents:\n%s' % '\n'.join(data))
            print('\n')
            with open(tmp_submit, 'w') as out_file:
                out_file.write('\n'.join(data))
            order.rename(bk_arc)
            tmp_submit.rename(final_submit)
            count += 1

    print('%d orders resubmitted' % count)


@Command(
        date=Spec('date to examine', OPTION, type=Date, radio='date'),
        email=Spec('send email to these addresses', MULTI),
        yesterday=Spec('examine yesterday', FLAG, target='date', radio='date', default=Date.today().replace(delta_day=-1)),
        )
def daily_digest(date, email):
    """
    print list of orders sent to FIS, and their detail
    """
    target = date or Date.today()
    print('target date: %r' % (target, ))
    target_period = Period(target.year, target.month, target.day)
    print('       period: %r' % (target_period, ))
    archive_order_list = get_files_to_process(ARCHIVE, target_period)
    process_order_list = get_files_to_process(ORDERS)
    lines = []
    if process_order_list:
        total_missed = len(process_order_list)
        columns, remainder = divmod(total_missed, 5)
        if remainder:
            columns += 1
        columns = min(columns, 5)
        template = '   ' + '%-16s ' * columns
        lines.append('FILES NOT PROCESSED')
        lines.extend([(template % row).rstrip() for row in grouped_by_column([o.filename for o in process_order_list], columns)])
        lines.append('===================')
        lines.extend(['',''])
    print('checking %d order files' % len(archive_order_list, ))
    orders = {}
    for order in archive_order_list:
        with open(order) as in_file:
            orders[order.filename] = in_file.read().strip().split('\n')
    lines.append('found %d records for %s' % (len(orders), target))
    # discard all orders not in date
    archive_order_list = [a for a in archive_order_list if a.filename in orders]
    if orders:
        total_orders = len(orders)
        if total_orders < 7:
            columns = 1
        else:
            columns, remainder = divmod(total_orders, 5)
            if remainder:
                columns += 1
            columns = min(columns, 5)
        template = '   ' + '%-16s ' * columns
        lines.append('')
        lines.extend([(template % row).rstrip() for row in grouped_by_column([o.filename for o in archive_order_list], columns)])
        lines.append('')
        for order in archive_order_list:
            order_lines = orders[order.filename]
            total_lines = len(order_lines)
            if total_lines < 7:
                columns = 1
            else:
                columns, remainder = divmod(total_orders, 5)
                if remainder:
                    columns += 1
                columns = min(columns, 3)
            template = '   ' + '%-25s ' * columns
            lines.append('=== %s ===' % (order.filename, ))
            lines.extend([(template % row).rstrip() for row in grouped_by_column(order_lines, columns)])
            lines.append('')
    if lines:
        if email:
            send_mail(email, target.strftime("portal orders - %Y-%m-%d"), '\n'.join(lines))
        else:
            echo('\n'.join(lines))

@Command(
        recipients=Spec('addresses to send mail to', MULTIREQ),
        subject=Spec('subject line', OPTION, force_default='process_openerp_orders mail test'),
        message=Spec('message body', OPTION, force_default='hope you got this!'),
        )
def test_mail(recipients, subject, message):
    sent, failed = send_mail(recipients, subject, message)
    if failed:
        error('failed to send to: %s' % ', '.join(failed))
        return Exit.UnknownError
    else:
        return Exit.Success

## helpers

heb = Var(lambda haystack: re.match('HE(\d\d\d)', haystack))

def get_files_to_process(path, target_period=None):
    """
    returns files that match \d*.txt from a specified target_period
    """
    # path must be a Path
    order_candidates = [
            fn
            for fn in path.glob('*.txt')
            if fn.stem.isdigit()
            ]
    if target_period is not None:
        target_orders = []
        for order in order_candidates:
            order_date = Date.fromtimestamp(order.stat().st_mtime)
            if order_date in target_period:
                target_orders.append(order)
        order_candidates = target_orders
    order_candidates.sort(key=lambda fn: int(fn.stem))
    return order_candidates

def process(order_file, errors):
    print('processing %s' % (order_file, ))
    try:
        order_no = int(order_file.stem)
        seq = BASE_SEQ + order_no % 10000
        with open(order_file) as in_file:
            order_lines = in_file.read().strip().split('\n')
        # order_lines looks like
        #   ['LUCKY-407B-900002',
        #    'RSD-041920',
        #    'PON-8172943',
        #    '002080 - 1 - 25 lb',
        #    '001045 - 1 - 25 lb', '']
        # customer login may have dashes, but transmitter numbers never will
        # so split on the right-most dash
        cust, trans = order_lines[0].strip().rsplit("-", 1)
        if trans == 'False':
            # something failed in the OpenERP export
            raise Exception('missing transmitter number')
        [rsd] = [xx for xx in order_lines if xx.startswith('RSD')] or ['dflt-%s' % TOMORROW]
        [pon] = [xx for xx in order_lines if xx.startswith('PON')] or ['dflt-0000000037']
        PON = pon.split('-')[-1]
        RSD = rsd.split('-')[-1]
        hdr = "C%s+P%s+D%s+" % (trans, PON, RSD)
        rec = hdr
        for line in order_lines[1:]:
            if line.startswith(('RSD','PON')):
                continue
            item, qty = [val.strip() for val in line.strip().split('-')][:2]
            if qty != "0":
                rec += "I%s+Q%s+" % (item, qty)
        extfile = EOE_PATH / "%s.ext" % seq
        with open(extfile, 'w') as out_file:
            out_file.write(rec)
        # file has been transferred to FIS
        # it now MUST be removed
        try:
            order_file.copy(ARCHIVE)
        finally:
            order_file.unlink()
    except Exception:
        exc_type, exc, _ = sys.exc_info()
        error_lines = format_exception_only(exc_type, exc)
        error_lines[0] = ("[%s]  " % order_file.filename) + error_lines[0]
        error(''.join(error_lines))
        errors.extend(error_lines)

Run()

# file formats

# recipient file format is scription's OrmFile
"""
users = ['ethan', 'emile', 'tony', 'ron']

[ethan]
email = ['ethan@stoneleaf.us', ]
text =  ['9715061961@vtext.com', ]

[emile]
email = ['emile@gmail.com', ]
text = ['6503433458@tmomail.net', ]

[tony]
email = ['tony@togo.net', ]
text = ['4159174115@msg.fi.google.com', ]

[ron]
email = ['rgiannini@sunridgefarms.com', ]
text = ['4086400865@vtext.com', ]

[availability]
ethan = "Mo-Fr:600-1900  Su:1700-2100"
emile = True
tony = True
ron = True

[availability.process_openerp_orders]
"""

# notification file format
"""
time contacted      address
2020-05-20 03:47    ethan@stoneleaf.us
"""

# text message carrier email addresses
"""
Alltel:          [10-digit number] at message.alltel.com
AT&T:            [10-digit number] at txt.att.net
Boost Mobile:    [10-digit number] at myboostmobile.com
Cricket Wireless [10-digit number] at mms.cricketwireless.net
Google Fi        [10-digit number] at msg.fi.google.com
Sprint:          [10-digit number] at messaging.sprintpcs.com
T-Mobile:        [10-digit number] at tmomail.net
U.S. Cellular:   [10-digit number] at email.uscc.net
Verizon:         [10-digit number] at vtext.com
Virgin Mobile:   [10-digit number] at vmobl.com

Could be handy if we need to have a script text-message us.

> Thanks! Any follow up on determining which service to email by
> telephone number? Particularly now that numbers are carrier
> independent?

There are a few services, none free:

data24-7.com: $12/mo + $0.006 per lookup -- API for immediate look-ups

realphonevalidation.com: request a quote -- batch processing of files

textmagic.com: $4/mo + $0.04 per lookup -- API for immediate look-ups
the $4 gives us a virtual phone number to send/receive messages with

Looks like textmagic is the best option so far.  If we go with them the fellow that helped answer my questions is
Peter (in case they care).
"""
