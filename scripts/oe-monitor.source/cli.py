#!/usr/local/bin/suid-python --py3

import sys; sys.path.insert(0, '/usr/local/bin/fis-oe3')

from scription import *
from antipathy import Path
from datetime import datetime
from dbf import DateTime
from collections import deque
from epithets import App, Frame, Pipe, Queue, QueueEmpty, sched, switch
from epithets import SINGLE, InsufficientSpace
from fis_oe.sql import SQL, TimeDelta
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

## API


@Command()
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
    orders = {}
    while True:
        if not orders:
            error('thread: check_status: waiting for an order')
            o = q.get()
        else:
            o = q.get(block=False)
        if o is not QueueEmpty:
            orders[o] = 'PLACED'
        for o, state in orders.items():
            error('thread: checking order', o)
            if state == 'PLACED':
                # see if it has been prepped
                error('thread: checking if prepped')
                if (ARCHIVE/'%s.txt' % o).exists():
                    orders[o] = 'PREPPED'
            if state == 'PREPPED':
                error('thread: checking if submitted')
                seq = BASE_SEQ + int(o) % 10000
                extfile = EOE_PATH / 'archive' / "%s.ext" % seq
                error('thread:   file', extfile)
                if extfile.exists():
                    orders[o] = 'SUBMITTED'
                    error('thread: done with', o)
            if orders[o] != state:
                q.put((o, orders[o]))
            time.sleep(1)
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


class MonitorApp(App):
    title = "OpenERP portal orders to EOE Submission Monitor"
    border_style = SINGLE
    size = 13, 88

    def __init__(self):
        super().__init__()
        self.grid = []
        self.waiting = deque()
        self.status_comm = Pipe()
        self.order_ids = set()
        sched.new_task(self.add_orders, label='add orders')
        sched.new_task(self.update_order_status, self.status_comm.one, label='update order status')
        sched.new_thread(check_status, self.status_comm.two, label='check order status', daemon=True)

    async def add_orders(self):
        while "user hasn't quit":
            for order in get_files_to_process(ORDERS):
                error('processing', order)
                oe_id = order.stem
                if oe_id not in self.order_ids:
                    error('  creating')
                    self.order_ids.add(oe_id)
                    w = self.main.add_widget(OrderInfo(oe_id))
                    sched.new_task(self.display_order, w, label='display order')
                    sched.new_task(w, label='order-%s'%oe_id)
                    await self.status_comm.one.put(oe_id)
            await sched.sleep(5)

    async def display_order(self, w):
        while not w.visible:
            try:
                self.main.build_contained(w)
            except InsufficientSpace:
                self.waiting.append(sched.current)
                sched.current = None
                await switch()
            else:
                self.grid.append(w)
                error('display_order() grid:', self.grid)
                # sched.call_soon(w.paint)

    def remove_order(self, w):
        """
        Remove order from data structures and move other orders to fill the gap.
        """
        if not w.visible:
            w.dismiss()
            return
        i = self.grid.index(w)
        self.grid.pop(i)
        empty = w.get_parent_yx()
        error('initial coordinates:', empty)
        error('saved coordinates:', w.saved_origin)
        w.dismiss()
        while i < len(self.grid):
            w = self.grid[i]
            error('moving widget', w)
            current = w.get_parent_yx()
            w.move_window(*empty)
            empty = current
            i += 1
        self.main.clear_primary = empty
        self.main.clear()
        self.main.refresh()
        if self.waiting:
            sched.ready.append(self.waiting.popleft())

    async def update_order_status(self, q):
        while True:
            order_id, msg = await q.get()
            sched.notify(order_id, msg)


class OrderInfo(Frame):
    border_style = SINGLE
    size = 3, 40
    visible = False

    def __init__(self, oe_id):
        super().__init__(title=oe_id)
        error('  initial setup of', oe_id)
        for xml_id, created, items, new_items in SQL(
                "SELECT partner_xml_id, create_date, item_ids, new_item_ids "
                "FROM fis_integration.online_order "
                "WHERE id=%s" % oe_id
                ).execute():
            break
        else:
            # nothing found, examine file
            with open(BASE_PATH/'%s.txt' % oe_id) as fh:
                order_lines = fh.read().strip().split('\n')
            xml_id, trans = order_lines[0].strip().rsplit("-", 1)
            items = new_items = 0
            created = DateTime()
            for line in order_lines[1:]:
                if line.startswith(('RSD','PON')):
                    continue
                item, qty = [val.strip() for val in line.strip().split('-')][:2]
                if qty != "0":
                    items += 1
        self.xml_id = xml_id
        self.created = created
        self.items = len(items) + len(new_items)
        self.oe_id = oe_id
        self.state = 'PLACED'

    async def __call__(self):
        """
        Ascertain current state.
        """
        sched.new_task(self.display, label='display-%s'%self.oe_id)
        while self.state != 'SUBMITTED':
            status = await sched.wait_notify(self.oe_id)
            error('received %r' % status)
            self.state = status
            if status == 'SUBMITTED':
                sched.call_later(3, app.remove_order, self)
                break
        sched.current = None

    async def display(self):
        while self.state != 'SUBMITTED':
            error('display: self.visible =', self.visible)
            self.paint()
            await sched.sleep(1)

    def paint(self):
        if self.visible:
            super().paint()
            self.add_string(0, 0, self.xml_id)
            # self.add_string(0, 26, 'oe-id# %6s' % self.oe_id)
            # self.add_string(1, 0, str(self.created))
            self.add_string(1, 0, 'items: %d' % self.items)
            self.add_string(0, 29, '%10s' % self.state)
            if self.created:
                # fancy-footwork for deficency in dbf.DateTime
                now = DateTime(datetime.utcnow(), tzinfo=UTC)
                self.add_string(2, 20, '%19s' % TimeDelta(now-self.created))
            self.refresh()

