import collections
import contextlib
import datetime
import functools
import itertools
import random
import sys
import types

for m in (collections, contextlib, datetime, functools, itertools, random, sys, types):
    sys.modules['enhlib.stdlib.%s' % m.__name__] = m

