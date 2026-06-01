#!/usr/local/bin/suid-python --py3

import sys; sys.path.insert(0, '/usr/local/bin/fis-oe3')

from scription import *
from antipathy import Path
from datetime import datetime
from dbf import DateTime
from collections import deque
from epithets import App, Frame, Pipe, Queue, QueueEmpty, sched, switch, Signal
from epithets import SINGLE, InsufficientSpace, NS, A_NORMAL, HORIZONTAL, NSEW
from fis_oe.sql import SQL, Table, TimeDelta
import logging
from pytz import UTC
import time


## globals

    # all order numbers must be in the 10000-19999 range or we have collisions
    # with other FIS-feeding processes

BASE_SEQ = 10000

EOE_PATH = Path("/mnt/11-111/home/eoe/")
BASE_PATH = Path("/home/openerp/sandbox/openerp/var/fis_integration/orders")
ORDERS = BASE_PATH
ARCHIVE = BASE_PATH / "archive"

logger = logging.getLogger('web-ingredients')
logging.basicConfig(filename='/var/log/oe-monitor.log', level=logging.DEBUG)
logging.getLogger('openerplib').setLevel(logging.INFO)
logger.info(str(DateTime.now()))

## API


@Command()
@Alias('oe-monitor')
def orders():
    """
    Show orders waiting to be submitted to EOE.
    """
    global app
    app = MonitorApp()
    app.run()


## helpers

def check_status(q):
    """
    Thread to access local and network drives.
    """
    logger = logging.getLogger('thread')
    orders = {}
    while True:
        if not orders:
            logger.info('check_status: waiting for an order')
            o = q.get()
        else:
            o = q.get(block=False)
        if o is not QueueEmpty:
            orders[o] = 'PLACED', None
        for o, (state, ts) in orders.items():
            logger.info('checking order %r', o)
            if state == 'PLACED':
                # see if it has been prepped
                logger.info('checking if prepped')
                target = ARCHIVE/'%s.txt' % o
                if target.exists():
                    ts = DateTime.fromtimestamp(target.stat().st_mtime)
                    orders[o] = 'PREPPED', ts
            if state == 'PREPPED':
                logger.info('checking if submitted')
                seq = BASE_SEQ + int(o) % 10000
                extfile = EOE_PATH / 'archive' / "%s.ext" % seq
                logger.info('file %r', extfile)
                if extfile.exists():
                    sts = DateTime.fromtimestamp(extfile.stat().st_mtime)
                    if sts > ts:
                        orders[o] = 'SUBMITTED', sts
                        logger.info('done with %r', o)
            if orders[o][0] != state:
                q.put((o, orders[o]))
        time.sleep(10)
        for o, s in list(orders.items()):
            if s == 'SUBMITTED':
                del orders[o]


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


# info we are interested in:
# - customer name (?)
# - order placed date/time
# - transmitter id
# - number of items
# - current state (OpenERP, Ready for EOE, Submitted to EOE)
# - current wait time


class CompletedOrders(Frame):
    """
    Show most recent completed orders.
    """
    size = 10, 35
    sticky = NS

    def __init__(self):
        super().__init__()
        self.value = []

    def on_order_complete(self, order):
        rows = self.inner_size.height - 2
        self.value.insert(0, order)
        while len(self.value) > rows:
            self.value.pop()
        self.paint()
        self.refresh()

    def paint(self, attr=A_NORMAL, cascade=True):
        super().paint(attr=attr, cascade=cascade)
        self.add_string(0, 1, 'FIS ID     items   submitted')
        self.add_string(1, 1, '---------- ----- -----------')
        for i, o in enumerate(self.value, start=2):
            self.add_string(i, 1, '%-10s %4s  %s' % (o.xml_id, o.items, o.completed.strftime('%m-%d %H:%M')))
        self.refresh()


class CurrentOrders(Frame):
    """
    Show processing orders.
    """
    sticky = NSEW


class OrderInfo(Frame):
    border_style = SINGLE
    size = 3, 37
    visible = False
    oe_order = False
    logger = logging.getLogger('order-info')
    layout = HORIZONTAL

    def __init__(self, oe_id):
        super().__init__(title=oe_id)
        self.logger.info('  initial setup of %r', oe_id)
        for xml_id, created, items, new_items in SQL(
                "SELECT partner_xml_id, create_date, item_ids, new_item_ids "
                "FROM fis_integration.online_order "
                "WHERE id=%s" % oe_id
                ).execute():
            self.oe_order = True
            break
        else:
            # nothing found, examine file
            with open(BASE_PATH/'%s.txt' % oe_id) as fh:
                order_lines = fh.read().strip().split('\n')
            xml_id, trans = order_lines[0].strip().rsplit("-", 1)
            items = []
            new_items = []
            created = DateTime()
            for line in order_lines[1:]:
                if line.startswith(('RSD','PON')):
                    continue
                item, qty = [val.strip() for val in line.strip().split('-')][:2]
                if qty != "0":
                    items.append(1)
        self.xml_id = xml_id
        self.created = created
        self.items = len(items) + len(new_items)
        self.oe_id = oe_id
        self.state = 'PLACED'
        self.oe_table = Table('fis_integration.online_order')
        

    async def __call__(self):
        """
        Ascertain current state.
        """
        sched.new_task(self.display, label='display-%s' % self.oe_id)
        while self.state != 'SUBMITTED':
            status, timestamp = await sched.wait_notify(self.oe_id)
            self.logger.info('received %r and %r', status, timestamp)
            self.state = status
            if status == 'PREPPED':
                if self.oe_order:
                    self.logger.info('updating %r with %r', self.oe_id, {'erp_file_date':timestamp})
                    self.oe_table.update_records(self.oe_id, {'erp_file_date':timestamp})
            if status == 'SUBMITTED':
                if self.oe_order:
                    self.logger.info('updating %r with %r', self.oe_id, {'eoe_file_date':timestamp})
                    self.oe_table.update_records(self.oe_id, {'eoe_file_date':timestamp})
                sched.call_later(11, app.remove_order, self, timestamp)
                break
        sched.current = None

    async def display(self):
        while True:
            self.logger.info('display: self.visible = %r', self.visible)
            self.paint()
            if self.state == 'SUBMITTED':
                break
            await sched.sleep(1)

    def paint(self, attr=A_NORMAL, cascade=True):
        if self.visible:
            super().paint(attr=attr, cascade=cascade)
            self.add_string(0, 0, self.xml_id or '')
            # self.add_string(0, 26, 'oe-id# %6s' % self.oe_id)
            # self.add_string(1, 0, str(self.created))
            self.add_string(1, 0, 'items: %d' % self.items)
            self.add_string(0, 26, '%10s' % self.state)
            if self.created:
                # fancy-footwork for deficency in dbf.DateTime
                now = DateTime(datetime.utcnow(), tzinfo=UTC)
                self.add_string(2, 17, '%19s' % TimeDelta(now-self.created))
            self.refresh()


class MonitorApp(App):
    title = "OpenERP portal orders to EOE Submission Monitor"
    border_style = SINGLE
    size = 13, 88
    layout = [CompletedOrders, CurrentOrders]
    logger = logging.getLogger('app')

    def __init__(self):
        super().__init__()
        self.grid = []
        self.waiting = deque()
        self.status_comm = Pipe()
        self.order_ids = set()
        sched.new_task(self.add_orders, label='add orders')
        sched.new_task(self.update_order_status, self.status_comm.conn1, label='update order status')
        sched.new_thread(check_status, self.status_comm.conn2, label='check order status', daemon=True)

    async def add_orders(self):
        current_frame = self.query_one(cls=CurrentOrders)
        while "user hasn't quit":
            for order in get_files_to_process(ORDERS):
                self.logger.info('processing %r', order)
                oe_id = int(order.stem)
                if oe_id not in self.order_ids:
                    self.logger.info('  creating')
                    self.order_ids.add(oe_id)
                    w = current_frame.add_widget(OrderInfo(oe_id))
                    sched.new_task(self.display_order, w, label='display order')
                    sched.new_task(w, label='order-%s'%oe_id)
                    await self.status_comm.conn1.put(oe_id)
            await sched.sleep(5)

    async def display_order(self, w):
        while not w.visible:
            try:
                w.build()
            except InsufficientSpace:
                self.logger.info('no space, in display queue')
                self.waiting.append(sched.current)
                sched.current = None
                await switch()
            else:
                self.grid.append(w)
                self.logger.info('display_order() grid: %r', self.grid)
                # sched.call_soon(w.paint)

    def remove_order(self, w, ts):
        """
        Remove order from data structures and move other orders to fill the gap.
        """
        current_frame = self.query_one(cls=CurrentOrders)
        w.completed = ts
        sched.call_soon(Signal('OrderComplete').notify, w)
        if not w.visible:
            w.dismiss()
            return
        i = self.grid.index(w)
        self.grid.pop(i)
        empty = w.origin
        w.dismiss()
        while i < len(self.grid):
            w = self.grid[i]
            self.logger.info('moving widget %r', w)
            current = w.origin
            w.move_window(*empty)
            empty = current
            i += 1
        current_frame.clear_primary = empty
        current_frame.clear()
        current_frame.refresh()
        if self.waiting:
            sched.ready.append(self.waiting.popleft())

    async def update_order_status(self, q):
        while True:
            order_id, (msg, timestamp) = await q.get()
            sched.notify(order_id, (msg, timestamp))



