'''
given ((potentially-multi)-output) truth table,
finds the right "clues" to describe  (in sum-of-products form)
'''

from math import log

tt = {
(0,0,0,0,0):1,
(0,0,0,0,1):0,
(0,0,0,1,0):1,
(0,0,0,1,1):1,
(0,0,1,0,0):1,
(0,0,1,0,1):1,
(0,0,1,1,0):1,
(0,0,1,1,1):1,
(0,1,0,0,0):1,
(0,1,0,0,1):1,
(0,1,0,1,0):1,
(0,1,0,1,1):1,
(0,1,1,0,0):1,
(0,1,1,0,1):1,
(0,1,1,1,0):1,
(0,1,1,1,1):1,
(1,0,0,0,0):0,
(1,0,0,0,1):0,
(1,0,0,1,0):0,
(1,0,0,1,1):0,
(1,0,1,0,0):0,
(1,0,1,0,1):0,
(1,0,1,1,0):0,
(1,0,1,1,1):0,
(1,1,0,0,0):0,
(1,1,0,0,1):0,
(1,1,0,1,0):0,
(1,1,0,1,1):0,
(1,1,1,0,0):0,
(1,1,1,0,1):0,
(1,1,1,1,0):0,
(1,1,1,1,1):0}


def entropy(table):
   if len(table)==0: return 0.0
   ones = float(sum(table.values()))/len(table)
   zeros = 1.0-ones 
   return sum(p*log(1.0/p) if p!=0 else 0.0 for p in (zeros,ones))

def sortby(table, i):
   return tuple({k:v for k,v in table.items() if k[i]==ki} for ki in (0,1))

def splittability(table,i):
   return entropy({k:i for i,st in enumerate(sortby(table,i)) for k in st.keys()})

def entropy_gain(table, i):
   if len(table)==0: return 0.0
   return entropy(table) - sum(entropy(st)*len(st) for st in sortby(table,i))/len(table)

#import random
def decision_tree(table,N):
   if len(table)==0: return '*' #won't happen
   if entropy(table)==0.0: return str(table.values()[0])
   maxgain, besti = max((entropy_gain(table, i),i) for i in range(N))
   if maxgain==0.0: maxsp, besti = max((splittability(table,i),i) for i in range(N))
   dt0, dt1 = (decision_tree(t,N) for t in sortby(table,besti))
   if dt0=='1' and dt1=='1': return 'one' #won't happen
   elif dt0=='1':
      if dt1=='0': return '~r%d' % besti #case dt1=='1' handled above already
      return '(~r%d | %s)' % (besti, dt1)
   elif dt1=='1':
      if dt0=='0': return 'r%d' % besti #case dt0=='1' handled above already
      return '(%s | r%d)' % (dt0, besti)
   elif dt0=='0' and dt1=='0': return 'zero' #won't happen
   elif dt0=='0': return 'r%d&%s' % (besti, dt1)
   elif dt1=='0': return '~r%d&%s' % (besti, dt0)
   else: return '(~r%d&%s | r%d&%s)' % (besti, dt0, besti, dt1)

def test(table, N, treestring):
   for k,v in {'&':' and ', '|':' or ', '~':' not '}.items():
      treestring=treestring.replace(k,v)
   for k,v in table.items():
      ts = treestring[:]
      for i in range(N)[::-1]:
         ts = ts.replace('r%d'%i, str(k[i])) 
      #print(ts) 
      if eval(ts) != v:
         print('mismatch! for %s, %d != %s' % (str(k), v, ts))
d = decision_tree(tt,5)
print('tree = %s' % d)
test(tt,5,d)
'''print(decision_tree(tt,5))'''
