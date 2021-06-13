def solution(a, qs):
    cut_tab = [False for _ in a]+[False]
    in_tab = [[] for _ in a]+[[]]
    out_tab = [[] for _ in a]+[[]]
    for i in range(len(qs)):
        q = qs[i]
        cut_tab[q[0]] = True
        in_tab[q[0]] += [i]
        cut_tab[q[1]] = True
        out_tab[q[1]] += [i]
    cut = []
    
    for i in range(len(cut_tab)):
        if cut_tab[i]:
            cut += [i]
    in_tab = [in_tab[i] for i in cut]
    out_tab = [out_tab[i] for i in cut]
    
    max_cut = [0 for _ in cut[:-1]] # si cut[i], alors max_cut[i] contient le max sur le troncon cut[i]:next_cut[i]
    for i in range(len(cut)-1):
        max_loc = 0
        for j in range(cut[i],cut[i+1]):
            max_loc = max(max_loc,a[j])
        max_cut[i] = max_loc
            
    
    rst = 0
    # il n'y a pas de query de longueur nulle
    q_answer = [0 for _ in qs]
    curr_q_index = []
    for i in range(len(max_cut)):
        next_q_index = []
        for j in range(len(curr_q_index)):
            q_j = curr_q_index[j]
            if qs[q_j][1] != cut[i]:
                q_answer[q_j] = max(q_answer[q_j],max_cut[i])
                next_q_index += [q_j]
            else:
                rst += q_answer[q_j]
        for j in range(len(in_tab[i])):
            q_j = in_tab[i][j]
            q_answer[q_j] = max(q_answer[q_j],max_cut[i])
            next_q_index += [q_j]
        curr_q_index = next_q_index
    for j in range(len(curr_q_index)):
        q_j = curr_q_index[j]
        rst += q_answer[q_j]
    return rst
    
        