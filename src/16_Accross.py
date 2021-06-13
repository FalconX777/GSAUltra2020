import queue

def solution(a, b):
    qa = queue.SimpleQueue()
    qb = queue.SimpleQueue()
    
    for i in range(len(a)-1,-1,-1):
        sa = a[i]
        qa.put_nowait(sa)
    for i in range(len(b)-1,-1,-1):
        sb = b[i]
        qb.put_nowait(sb)
    
    nb_rounds = 0
    
    while qa.qsize()>0 and qb.qsize()>0:
        sa = qa.get_nowait()
        sb = qb.get_nowait()
        if sa == 'R':
            if sb == 'R': # tie
                qa.put_nowait(sa)
                qb.put_nowait(sb)
            elif sb == 'P': # b win
                qb.put_nowait(sa)
                qb.put_nowait(sb)
            else: # a win
                qa.put_nowait(sb)
                qa.put_nowait(sa)
        elif sa == 'P':
            if sb == 'P': # tie
                qa.put_nowait(sa)
                qb.put_nowait(sb)
            elif sb == 'S': # b win
                qb.put_nowait(sa)
                qb.put_nowait(sb)
            else: # a win
                qa.put_nowait(sb)
                qa.put_nowait(sa)
        else:
            if sb == 'S': # tie
                qa.put_nowait(sa)
                qb.put_nowait(sb)
            elif sb == 'R': # b win
                qb.put_nowait(sa)
                qb.put_nowait(sb)
            else: # a win
                qa.put_nowait(sb)
                qa.put_nowait(sa)
        nb_rounds += 1
    return nb_rounds
    