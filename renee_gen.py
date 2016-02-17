def wheel_state(lss, rss, fb, lb, bb, rb):
   '''left sensors[0,1,2]           [2=MSB]
      right sensors[0,1,2]          [2=MSB]
      front,left,back,right bumpers [active low]
      => returns value of left wheel: 'F','S',or 'R'
   '''
   fb,lb,bb,rb = (not x for x in (fb,lb,bb,rb)) #undo active low
   #print fb,lb,bb,rb
   if not(fb or lb or bb or rb):
      lnum = sum(2**i * c for i,c in enumerate(lss))
      rnum = sum(2**i * c for i,c in enumerate(rss))
      #print(rnum,lnum, 's' if rnum==0 else 'F' if lnum<=rnum else 'S')
      if rnum==0: return 'S'
      return 'F' if lnum<=rnum else 'S'
   elif (fb and bb) or (lb and rb):
      return 'S'
   else:
      if lb: return 'R' if not bb else 'F'
      elif rb: return 'S' #no matter what bb is
      elif fb: return 'R'
      elif bb: return 'F'
      else: return 'S'

led7s = {'F':(1,0,0,0,1,1,1),
         'S':(1,0,1,1,0,1,1),
         'R':(0,0,0,0,1,0,1)} #not active low (will become active low in next line)
led7s = {k:tuple(1- x for x in v) for k,v in led7s.items()} #now active low

def segments(rss, lss, fb, lb, bb, rb): # all 14 (from 2 hex displays)
   return led7s[wheel_state(rss, lss, fb, rb, bb, lb)] + \
          led7s[wheel_state(lss, rss, fb, lb, bb, rb)]    # left wheel

B = (0,1); N=10
ins = [()]
for n in range(N):
   ins = [i+(j,) for i in ins for j in B]

varnames = {'r0':'rs[0]','r1':'rs[1]','r2':'rs[2]',
            'r3':'ls[0]','r4':'ls[1]','r5':'ls[2]',
            'r6':'fb','r7':'lb','r8':'bb','r9':'rb'}
for i in range(7):
   varnames['led%d '%i] = 'lwd[%d] '%i
   varnames['led%d '%(i+7)] = 'rwd[%d] '%i
#print(varnames)
def super_replace(string, replacements):
   for k,v in replacements.items():
      string = string.replace(k,v)
   return string

with open('woah','w') as f:
   for i in [(0,0,0,0,0,0,1,1,1,1),
             (0,0,0,0,0,1,1,1,1,1),
             (0,0,0,0,1,0,1,1,1,1)]:#ins:
      f.write('%s %s\n' % (str(i).replace(', ',''),str(segments(i[:3],i[3:6],*i[6:10])).replace(', ','')))

import decision_tree
for j in range(14):
   myttt = {i:int(segments(i[:3],i[3:6],*i[6:10])[j]) for i in ins}
   line = 'assign led%d = %s;' % (j,decision_tree.decision_tree(myttt,N))
   test = super_replace(line.split('=')[1], {'|':' or ', '&':' and ', '~':' not '})
   for i in ins:
      if not segments(i[:3],i[3:6],*i[6:10])[j] == eval(super_replace(test[:-1],{'r%d'%jj:str(i[jj]) for jj in range(10)})):
         print('!', i)
   line = super_replace(line, varnames)

