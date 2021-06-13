import math
import sys
sys.setrecursionlimit(10**9) 

def dicho(t, v):
    a = 0
    b = len(t)
    if b == 0:
        return False
    while True:
        m = (a + b) // 2
        if a == m:
            if t[a] == v:
                return True
            return False
        if t[m] > v:
            b = m
        else:
            a = m

def solution(s,db=[],max_prime=9999,rst_db=dict()):
    # Db initialization
    if len(db) == 0:
        db_prime = [2,3,5,7,11,13,17,19]
        for i in range(20,10000):
            prime = True
            k = 0
            while k<len(db_prime) and db_prime[k]<=int(math.sqrt(i)):
                if i%db_prime[k] == 0:
                    prime = False
                    break
                else:
                    k += 1
            if prime:
                db_prime += [i]
        db = [[] for _ in range(4)]
        k = 0
        for i in range(4):
            while k<len(db_prime) and db_prime[k] <= 10**(i+1):
                db[i] += [db_prime[k]]
                k += 1
    
    # Quick cases
    if len(s)<5:
        if int(s)<max_prime and dicho(db[len(s)-1],int(s)):
            return int(s)
        
    # Pattern finding
    pat = []
    max_pat = 0
    for i in range(int(math.log(max_prime+0.5,10))+1):
        for j in range(len(s)-i):
            if s[j] != '0':
                prime = int(s[j:j+i+1])
                if prime<max_prime and dicho(db[i],prime):
                    pat += [[j,i+1]]
                    max_pat = max(max_pat,prime)
    
    # Rst_db
    if rst_db.get(s) != None:
        rst_tab = rst_db.get(s)
        for i in range(len(rst_tab)):
            dbrst,maxdb_prime = rst_tab[i]
            if max_pat < maxdb_prime:
                rst_tab.insert(i,[dbrst,max_prime])
                return dbrst
    
    # Recursivité
    rst = 0
    for p in pat:
        prime = int(s[p[0]:p[0]+p[1]])
        sub_sol = solution(s[:p[0]]+s[p[0]+p[1]:],db,prime,rst_db)
        rst = max(rst,sub_sol+prime)
        
    if rst_db.get(s) != None:
        rst_db[s].insert(len(rst_db[s]),[rst,max_prime])
    else:
        rst_db[s] = [[rst,max_prime]]
    return rst