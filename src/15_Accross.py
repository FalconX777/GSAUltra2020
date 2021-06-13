import math

def dicho(t, v):
    a = 0
    b = len(t)
    if b == 0:
        return 0
    while True:
        m = (a + b) // 2
        if a == m:
            if t[a][0] >= v:
                return a
            return a+1
        if t[m][0] > v:
            b = m
        else:
            a = m

def find_block(block,chunks):
    index,length = block[0],block[1]
    if length <= 0:
        return -1,-1
    chunk = chunks[int(math.log(length,2))]
    ind = dicho(chunk,index)
    if len(chunk)>ind and chunk[ind][0] == index:
        return int(math.log(length,2)),ind
    return -1,-1
    

def solution(n, rs):
    chunks = [[] for _ in range(int(math.log(n,2))+1)]
    chunks[-1] += [[0,n,[-1,0],[-1,0]]] # (index,length,next_block,previous_block)
    ri_d = dict() # key=request_index, value=(index,length,next_block,previous_block)
    ind_d = dict() # key=index, value=request_index
    curr_ri = 0
    for r in rs:
        if r[0] == 'I':
            # trouver le block à allouer
            ck_min = int(math.log(r[1],2))
            i_min = n
            j_min = 0
            for ck_ind in range(int(math.log(r[1],2)),len(chunks)):
                chunk = chunks[ck_ind]
                for j in range(len(chunk)):
                    if chunk[j][1]>=r[1] and chunk[j][0]<i_min:
                        i_min = chunk[j][0]
                        j_min = j
                        ck_min = ck_ind
                        break
            alloc = chunks[ck_min].pop(j_min)
                
            # replacer le free block
            free_block = [alloc[0]+r[1],alloc[1]-r[1],[alloc[0],r[1]],alloc[3]]
            if free_block[1]>0:
                chunk = chunks[int(math.log(free_block[1],2))]
                index = dicho(chunk,free_block[0])
                chunk.insert(index,free_block)
                ri_d[str(curr_ri)] = [alloc[0],r[1],alloc[2],[free_block[0],free_block[1]]]
                ind_d[str(alloc[0])] = curr_ri
            else:
                ri_d[str(curr_ri)] = [alloc[0],r[1],alloc[2],alloc[3]]
                ind_d[str(alloc[0])] = curr_ri
            # modifier l'info dans le block précédent
            pri = ind_d.get(str(alloc[2][0]))
            if pri != None: # if it is allocated
                ri_d[str(pri)][3][1] = r[1]
            else: # if it is free (impossible)
                ck_ind,ind = find_block(alloc[2],chunks)
                if ck_ind != -1:
                    chunks[ck_ind][ind][3][1] = r[1]
            # modifier l'info dans le block suivant (s'il change)
            nri = ind_d.get(str(alloc[3][0]))
            if nri != None: # if it is allocated
                if free_block[1]>0:
                    ri_d[str(nri)][2][0] = free_block[0]
                    ri_d[str(nri)][2][1] = free_block[1]
            else: # if it is free (impossible)
                ck_ind,ind = find_block(alloc[3],chunks)
                if ck_ind != -1:
                    if free_block[1]>0:
                        chunks[ck_ind][ind][2][0] = free_block[0]
                        chunks[ck_ind][ind][2][1] = free_block[1]
            # update curr_ri
            curr_ri += 1
        else:
            
            (index,length,prev_blk,nxt_blk) = ri_d.pop(str(r[1]))
            ind_d.pop(str(index))
            nck_ind = -2
            pck_ind = -2
            # modifier l'info dans le block précédent
            pri = ind_d.get(str(prev_blk[0]))
            if pri != None: # if it is allocated
                pck_ind = int(math.log(length,2))
                pind = dicho(chunks[pck_ind],index)
                chunks[pck_ind].insert(pind,[index,length,prev_blk,nxt_blk])
                # rien à faire dans le block prec
            else: # if it is free
                pck_ind,pind = find_block(prev_blk,chunks)
                nck_ind,nind = find_block(nxt_blk,chunks)
                if pck_ind != -1: # Fusion
                    chunks[pck_ind][pind][1] += length
                    chunks[pck_ind][pind][3] = nxt_blk
                    # modifier l'info de fusion dans le block précédent
                    pri = ind_d.get(str(chunks[pck_ind][pind][2][0]))
                    if pri != None: # if it is allocated
                        ri_d[str(pri)][3] = [chunks[pck_ind][pind][0],chunks[pck_ind][pind][1]]
                    else: # if it is free
                        ck_ind,ind = find_block(chunks[pck_ind][pind][2],chunks)
                        if ck_ind != -1:
                            chunks[ck_ind][ind][3] = [chunks[pck_ind][pind][0],chunks[pck_ind][pind][1]]
                    # replacer le block
                    if chunks[pck_ind][pind][1] >= 2**(pck_ind+1):
                        fus_block = chunks[pck_ind].pop(pind)
                        pck_ind = int(math.log(fus_block[1],2))
                        pind = dicho(chunks[pck_ind],fus_block[0])
                        chunks[pck_ind].insert(pind,fus_block)
                    # update the current block
                    (index,length,prev_blk,nxt_blk) = chunks[pck_ind][pind]
                else: # there is no previous block (beginning of memory)
                    pck_ind = int(math.log(length,2))
                    pind = dicho(chunks[pck_ind],index)
                    chunks[pck_ind].insert(pind,[index,length,prev_blk,nxt_blk])
                    # rien à faire dans le block prec
            # modifier l'info dans le block suivant

            
            nri = ind_d.get(str(nxt_blk[0]))
            if nri != None: # if it is allocated
                ri_d[str(nri)][2][0] = index
                ri_d[str(nri)][2][1] = length
            else:
                nck_ind,nind = find_block(nxt_blk,chunks)
                if nck_ind != -1: # Fusion
                    (nindex,nlength,nprev_blk,nnxt_blk) = chunks[nck_ind][nind]
                    chunks[pck_ind][pind][1] += nlength
                    chunks[pck_ind][pind][3] = nnxt_blk
                    # modifier l'info de fusion dans le block suivant
                    nri = ind_d.get(str(chunks[pck_ind][pind][3][0]))
                    if nri != None: # if it is allocated
                        ri_d[str(nri)][2] = [chunks[pck_ind][pind][0],chunks[pck_ind][pind][1]]
                    else: # if it is free
                        ck_ind,ind = find_block(nnxt_blk,chunks)
                        if ck_ind != -1:
                            chunks[ck_ind][ind][2] = [chunks[pck_ind][pind][0],chunks[pck_ind][pind][1]]
                    # modifier l'info de fusion dans le block précédent
                    pri = ind_d.get(str(chunks[pck_ind][pind][2][0]))
                    if pri != None: # if it is allocated
                        ri_d[str(pri)][3] = [chunks[pck_ind][pind][0],chunks[pck_ind][pind][1]]
                    else: # if it is free
                        ck_ind,ind = find_block(chunks[pck_ind][pind][2],chunks)
                        if ck_ind != -1:
                            chunks[ck_ind][ind][3] = [chunks[pck_ind][pind][0],chunks[pck_ind][pind][1]]
                    # replacer le block
                    if chunks[pck_ind][pind][1] >= 2**(pck_ind+1):
                        fus_block = chunks[pck_ind].pop(pind)
                        pck_ind = int(math.log(fus_block[1],2))
                        pind = dicho(chunks[pck_ind],fus_block[0])
                        chunks[pck_ind].insert(pind,fus_block)
                    # pop
                    nck_ind,nind = find_block([nindex,nlength],chunks)
                    chunks[nck_ind].pop(nind)
            
    rst = 0
    for key,value in ind_d.items():
        rst += int(key)*value
    return rst