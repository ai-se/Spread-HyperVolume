from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division
from random import uniform

"Hyper volume estimation"
"RAISE LAB"
__author__ = "Zhe Yu"

###### something you might want to modify to fit your own code #######

"definition of Better"
def Better(a,b):
    return a<b

"get objective value of candidate; returns a list"
def getobj(a):
    return a.getobj()

#######################################################################



"is a binary dominate b?"
def is_bd(a,b):
    try:
        obj_a=getobj(a)
    except:
        obj_a=a
    try:
        obj_b=getobj(b)
    except:
        obj_b=b
    if obj_a==obj_b:
        return False
    for i in xrange(a.objnum):
        if Better(obj_b[i],obj_a[i]):
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
    m=len(getobj(frontier[0]))
    for i in xrange(sample):
        pebble=[uniform(min[k],max[k]) for k in xrange(m)]
        if inbox(pebble,frontier):
            count=count+1
    return count/(sample)

