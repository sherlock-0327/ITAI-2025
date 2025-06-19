def Trans(S):
    res=0
    for c in S:
        if c<'0' or c>'9':
            return 0
        res=res*10+(ord(c)-48)
    return res

N=Trans(input())
while N==0:
    print("Invalid input, please try again")
    N=Trans(input())

pos=[0]*N
result=[]
def DFS(t,limC,limL,limR):
    global result
    if t==N:
        result+=[pos.copy()]
        return
    lim=limC|limL|limR
    for i in range(0,N):
        if(t>0 or(i<<1)<N)and(lim>>i&1)==0:
            pos[t]=i
            DFS(t+1,limC|1<<i,(limL|1<<i)>>1,(limR<<1|1<<i+1)&(1<<N)-1)

import time
StartTime=time.process_time()
DFS(0,0,0,0)
s=len(result)
for i in range(s-1,-1,-1):
    result+=[[N-x-1 for x in result[i]]]
EndTime=time.process_time()

for r in result:
    print(r)
print(len(result),end=" solutions in totals\n")

import sys
print(EndTime-StartTime,end=" seconds for searching",file=sys.stderr)