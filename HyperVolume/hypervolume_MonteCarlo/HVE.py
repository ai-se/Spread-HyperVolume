from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division
from random import uniform

"Hyper volume estimation"
"RAISE LAB"
__author__ = "Zhe Yu"


"is a binary dominate b? smaller is better"
def is_bd(a,b):
    try:
        obj_a=a.getobj()
    except:
        obj_a=a
    try:
        obj_b=b.getobj()
    except:
        obj_b=b
    if obj_a==obj_b:
        return False
    for i in xrange(a.objnum):
        if obj_b[i]<obj_a[i]:
            return False
    return True

"is the peddle inside the hyper volume"
def inbox(pebble,frontier):
    for candidate in frontier:
        if is_bd(candidate,pebble):
            return True
    return False


"estimate hyper volumn of frontier"
def hve(frontier,min,max,sample=100000):
    count=0
    m=frontier[0].objnum
    for i in xrange(sample):
        pebble=[uniform(min[k],max[k]) for k in xrange(m)]
        if inbox(pebble,frontier):
            count=count+1
    return count/(sample)

