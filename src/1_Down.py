# Version submitted

from fractions import Fraction as frac

def pb_win(i,j,skl_tab):
        return frac(skl_tab[i],skl_tab[i]+skl_tab[j])

def proba_all(skl_tab,table={}):
    rst = []
    for i in range(len(skl_tab)):
        skl_tab[0], skl_tab[i] = skl_tab[i], skl_tab[0] 
        rst += [proba(skl_tab,table=table)]
        skl_tab[0], skl_tab[i] = skl_tab[i], skl_tab[0] 
    return rst

def proba(skl_tab,table={}):
    if len(skl_tab) == 2:
        return pb_win(0,1,skl_tab)
    elif len(skl_tab) == 4:
        if str(skl_tab) in table:
            return table[str(skl_tab)]
        pb1 =  pb_win(0,1,skl_tab)*(pb_win(0,2,skl_tab)*pb_win(2,3,skl_tab) + pb_win(0,3,skl_tab)*pb_win(3,2,skl_tab))
        pb2 =  pb_win(0,2,skl_tab)*(pb_win(0,1,skl_tab)*pb_win(1,3,skl_tab) + pb_win(0,3,skl_tab)*pb_win(3,1,skl_tab))
        pb3 =  pb_win(0,3,skl_tab)*(pb_win(0,1,skl_tab)*pb_win(1,2,skl_tab) + pb_win(0,2,skl_tab)*pb_win(2,1,skl_tab))
        pb_andy = frac(1,3)*(pb1+pb2+pb3)
        
        table[str(skl_tab)] = pb_andy
        return pb_andy
    elif len(skl_tab) == 8:
        # parcourir les parties à 4 éléments de [0,7]
        pb = [] # garde la proba de win de Andy pour chaque configuration
        index_l = [0,1,2,3]
        index_r = [4,5,6,7]
        skl_tab_l = skl_tab[:4].copy()
        skl_tab_r = skl_tab[4:].copy()

        for i in range(-1,4):
            if i != -1:
                index_l[3], index_r[i] = index_r[i], index_l[3]
                skl_tab_l[3], skl_tab_r[i] = skl_tab_r[i], skl_tab_l[3]
            for j in range(i,4):
                if j != i:
                    index_l[2], index_r[j] = index_r[j], index_l[2]
                    skl_tab_l[2], skl_tab_r[j] = skl_tab_r[j], skl_tab_l[2]
                for k in range(j,4):
                    if k != j:
                        index_l[1], index_r[k] = index_r[k], index_l[1]
                        skl_tab_l[1], skl_tab_r[k] = skl_tab_r[k], skl_tab_l[1]
                    
                    pb_all = proba_all(skl_tab_r,table=table)
                    if str(skl_tab) in table:
                        pb_andy = table[str(skl_tab)]
                    else:
                        pb_andy = proba(skl_tab_l,table)
                    
                    pb += [pb_andy*(pb_win(0,index_r[0],skl_tab)*pb_all[0]+pb_win(0,index_r[1],skl_tab)*pb_all[1]+pb_win(0,index_r[2],skl_tab)*pb_all[2]+pb_win(0,index_r[3],skl_tab)*pb_all[3])]

                    if k != j:
                        index_l[1], index_r[k] = index_r[k], index_l[1]
                        skl_tab_l[1], skl_tab_r[k] = skl_tab_r[k], skl_tab_l[1]
                if j != i:
                    index_l[2], index_r[j] = index_r[j], index_l[2]
                    skl_tab_l[2], skl_tab_r[j] = skl_tab_r[j], skl_tab_l[2]
            if i != -1:
                index_l[3], index_r[i] = index_r[i], index_l[3]
                skl_tab_l[3], skl_tab_r[i] = skl_tab_r[i], skl_tab_l[3]
        rst = frac(0,1)
        for p in pb:
            rst += p
        rst = frac(1,len(pb))*rst
        return rst
    elif len(skl_tab) == 16:
        # parcourir les parties à 8 éléments de [0,15]
        pb = [] # garde la proba de win de Andy pour chaque configuration
        index_l = [0,1,2,3,4,5,6,7]
        index_r = [8,9,10,11,12,13,14,15]
        skl_tab_l = skl_tab[:8].copy()
        skl_tab_r = skl_tab[8:].copy()

        for i in range(-1,8):
            if i != -1:
                index_l[7], index_r[i] = index_r[i], index_l[7]
                skl_tab_l[7], skl_tab_r[i] = skl_tab_r[i], skl_tab_l[7]
            for j in range(i,8):
                if j != i:
                    index_l[6], index_r[j] = index_r[j], index_l[6]
                    skl_tab_l[6], skl_tab_r[j] = skl_tab_r[j], skl_tab_l[6]
                for k in range(j,8):
                    if k != j:
                        index_l[5], index_r[k] = index_r[k], index_l[5]
                        skl_tab_l[5], skl_tab_r[k] = skl_tab_r[k], skl_tab_l[5]
                    for l in range(k,8):
                        if l != k:
                            index_l[4], index_r[l] = index_r[l], index_l[4]
                            skl_tab_l[4], skl_tab_r[l] = skl_tab_r[l], skl_tab_l[4]
                        for m in range(l,8):
                            if m != l:
                                index_l[3], index_r[m] = index_r[m], index_l[3]
                                skl_tab_l[3], skl_tab_r[m] = skl_tab_r[m], skl_tab_l[3]
                            for n in range(m,8):
                                if n != m:
                                    index_l[2], index_r[n] = index_r[n], index_l[2]
                                    skl_tab_l[2], skl_tab_r[n] = skl_tab_r[n], skl_tab_l[2]
                                for o in range(n,8):
                                    if o != n:
                                        index_l[1], index_r[o] = index_r[o], index_l[1]
                                        skl_tab_l[1], skl_tab_r[o] = skl_tab_r[o], skl_tab_l[1]
                                    
                                    pb_all = proba_all(skl_tab_r,table=table)
                                    if str(skl_tab) in table:
                                        pb_andy = table[str(skl_tab)]
                                    else:
                                        pb_andy = proba(skl_tab_l,table)
                                        table[str(skl_tab)] = pb_andy
                                    
                                    pb += [pb_andy*(pb_win(0,index_r[0],skl_tab)*pb_all[0]+pb_win(0,index_r[1],skl_tab)*pb_all[1]+pb_win(0,index_r[2],skl_tab)*pb_all[2]+pb_win(0,index_r[3],skl_tab)*pb_all[3])]

                                    
                                    if o != n:
                                        index_l[1], index_r[o] = index_r[o], index_l[1]
                                        skl_tab_l[1], skl_tab_r[o] = skl_tab_r[o], skl_tab_l[1]
                                if n != m:
                                    index_l[2], index_r[n] = index_r[n], index_l[2]
                                    skl_tab_l[2], skl_tab_r[n] = skl_tab_r[n], skl_tab_l[2]
                            if m != l:
                                index_l[3], index_r[m] = index_r[m], index_l[3]
                                skl_tab_l[3], skl_tab_r[m] = skl_tab_r[m], skl_tab_l[3]
                        if l != k:
                            index_l[4], index_r[l] = index_r[l], index_l[4]
                            skl_tab_l[4], skl_tab_r[l] = skl_tab_r[l], skl_tab_l[4]
                    if k != j:
                        index_l[5], index_r[k] = index_r[k], index_l[5]
                        skl_tab_l[5], skl_tab_r[k] = skl_tab_r[k], skl_tab_l[5]
                if j != i:
                    index_l[6], index_r[j] = index_r[j], index_l[6]
                    skl_tab_l[6], skl_tab_r[j] = skl_tab_r[j], skl_tab_l[6]
            if i != -1:
                index_l[7], index_r[i] = index_r[i], index_l[7]
                skl_tab_l[7], skl_tab_r[i] = skl_tab_r[i], skl_tab_l[7]
        rst = frac(0,1)
        for p in pb:
            rst += p
        rst = frac(1,len(pb))*rst
        return rst

def solution(skills):
    l = len(skills)
    skl_tab = [0 for _ in range(l)]
    i = 1
    for name,skill in skills.items():
        if name == 'Andy':
            skl_tab[0] = skill
        else:
            skl_tab[i] = skill
            i+=1
    rst = str(proba(skl_tab)).split('/')
    return rst[0]+rst[1]
