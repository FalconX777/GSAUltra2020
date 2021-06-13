def solution(ts, w):
    # Database manager   
    depth_tab = [(t[0]==-1)-1 for t in ts]
    depth_max = 0
    children_tab = [[] for _ in ts]
    checked = [False for _ in ts]
    for i in range(len(ts)-1,-1,-1):
        curr_i = i
        i_tab_loc = []
        while not checked[curr_i] and ts[curr_i][0] != -1:
            i_tab_loc += [curr_i]
            p = ts[curr_i][0]
            children_tab[p] += [curr_i]
            checked[curr_i] = True
            curr_i = p
        depth = depth_tab[curr_i]
        for j in range(len(i_tab_loc)):
             depth_tab[i_tab_loc[j]] = depth + len(i_tab_loc) - j
        depth_max = max(depth_max,depth + len(i_tab_loc))
    
    index_order = [[] for _ in range(depth_max+1)]    
    for i in range(len(depth_tab)):
        index_order[depth_tab[i]] += [i]
    
    weight = [1 for _ in ts]
    for d in range(len(index_order)-1,-1,-1):
        for i in index_order[d]:
            children = children_tab[i]
            for child in children:
                weight[i] += weight[child]
                    
    sol = [[0 for _ in range(min(w+1,weight[i]+1))] for i in range(len(ts))]
    for d in range(len(index_order)-1,-1,-1):
        for i in index_order[d]:
            children = children_tab[i]
            if len(children) == 0:
                sol[i][0] = ts[i][1]
            else:
                min_max = [0 for _ in range(min(w+1,weight[i]+1))]
                j_tab = [j for j in range(len(children))]
                j_tab = sorted(j_tab,key=lambda j:sol[children[j]][0])
                j_max = j_tab[-1]
                min_max[0] = sol[children[j_max]][0]
                w_tab = [0 for _ in range(len(children))]
                for w_loc in range(1,min(w+1,weight[i]+1)):
                    w_tab[j_max] += 1
                    
                    j_0 = len(j_tab)-1
                    child = children[j_tab[j_0]]
                    w_child = w_tab[j_tab[j_0]]
                    child_n = children[j_tab[max(j_0-1,0)]]
                    w_child_n = w_tab[j_tab[max(j_0-1,0)]]
                    while j_0>0 and sol[child][min(w_child,len(sol[child])-1)]<sol[child_n][min(w_child_n,len(sol[child_n])-1)]:
                        j_tab[j_0], j_tab[j_0-1] = j_tab[j_0-1], j_tab[j_0]
                        j_0 -= 1
                        child = children[j_tab[j_0]]
                        w_child = w_tab[j_tab[j_0]]
                        child_n = children[j_tab[max(j_0-1,0)]]
                        w_child_n = w_tab[j_tab[max(j_0-1,0)]]
                    j_max = j_tab[-1]
                    min_max[w_loc] = sol[children[j_max]][min(w_tab[j_max],len(sol[children[j_max]])-1)]
                sol[i][0] = ts[i][1]+min_max[0]
                if d>0:
                    for w_loc in range(1,min(w+1,weight[i]+1)): 
                        sol[i][w_loc] = min(ts[i][1]+min_max[w_loc],min_max[w_loc-1])
                elif min(w,weight[i])>0:
                    w_loc = min(w,weight[i])
                    sol[i][w_loc] = min(ts[i][1]+min_max[w_loc],min_max[w_loc-1]) 
    return sol[0][-1]