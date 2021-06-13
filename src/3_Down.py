from fractions import Fraction as frac

def proba_child_dvt(g,children,rst_tab,pb_tot_tab,proba_matrix,wabbits):
    pb_tot_loc = [1 for _ in children]
    rst_loc = [0 for _ in children]
    
    for i in range(len(children)-1,-1,-1):
        child = children[i]
        if wabbits[child][1] == 'G':
            g_tab = [2]
        elif wabbits[child][1] == '?':
            g_tab = [0,1,2]
        else:
            g_tab = [0,1]
        
        if i == len(children)-1:
            pb_loc = 0
            for g_loc in g_tab:
                rst_loc[i] += (rst_tab[child][g_loc])*proba_matrix[g][g_loc]*pb_tot_tab[child][g_loc]
                pb_loc += proba_matrix[g][g_loc]*pb_tot_tab[child][g_loc]
            pb_tot_loc[i] = pb_loc
            if pb_loc > 0:
                rst_loc[i] /= pb_loc
        
        else:
            next_i = min(i+1,len(children)-1)
            next_child = children[next_i]

            pb_loc = 0
            for g_loc in g_tab:
                rst_loc[i] += (rst_tab[child][g_loc])*proba_matrix[g][g_loc]*pb_tot_tab[child][g_loc]
                pb_loc += proba_matrix[g][g_loc]*pb_tot_tab[child][g_loc]
            pb_tot_loc[i] = pb_loc
            if pb_loc > 0:
                rst_loc[i] /= pb_loc
                rst_loc[i] += rst_loc[next_i]
            pb_tot_loc[i] *= pb_tot_loc[next_i]
        
    return rst_loc[0], pb_tot_loc[0]

def proba_dvt(wabbits,pb):
    proba_matrix = [[(1-pb)**2,2*pb*(1-pb),pb**2],
                    [pb*(1-pb),pb**2+(1-pb)**2,pb*(1-pb)],
                    [pb**2,2*pb*(1-pb),(1-pb)**2]]

    depth_tab = [(wabbit[0]==-1)-1 for wabbit in wabbits]
    depth_max = 0
    children_tab = [[] for _ in wabbits]
    checked = [False for _ in wabbits]
    for i in range(len(wabbits)-1,-1,-1):
        curr_i = i
        i_tab_loc = []
        while not checked[curr_i] and wabbits[curr_i][0] != -1:
            i_tab_loc += [curr_i]
            p = wabbits[curr_i][0]
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
    
    # Initialization 
    rst_tab = [[0,0,0] for _ in range(len(wabbits))] # [[nb_green(wabbits[i:] | geno(i)==k) for k] for i]
    pb_tot_tab = [[0,0,0] for _ in range(len(wabbits))] # P(geno(i) = k) pour wabbits[i:]
    
    # General loop
    for d in range(len(index_order)-1,-1,-1):
        for i in index_order[d]:
            # Liste des enfants
            children = children_tab[i]
            # Fin de lignee
            if len(children) == 0:
                if wabbits[i][1] == 'G':
                    rst_tab[i] = [frac(0,1),frac(0,1),frac(1,1)]
                    pb_tot_tab[i] = [frac(0,1),frac(0,1),frac(1,1)]
                elif wabbits[i][1] == '?':  
                    rst_tab[i] = [frac(0,1),frac(0,1),frac(1,1)]
                    pb_tot_tab[i] = [frac(1,1),frac(1,1),frac(1,1)]
                else:
                    rst_tab[i] = [frac(0,1),frac(0,1),frac(1,1)]
                    pb_tot_tab[i] = [frac(1,1),frac(1,1),frac(0,1)]

            # Cas général
            else:
                if wabbits[i][1] == 'G':
                    g_tab = [2]
                elif wabbits[i][1] == '?':
                    g_tab = [0,1,2]
                else:
                    g_tab = [0,1]
                for g in g_tab:
                    rst_tab[i][g], pb_tot_tab[i][g] = proba_child_dvt(g,children,rst_tab,pb_tot_tab,proba_matrix,wabbits)
                rst_tab[i][2] += 1
            
    # Case i = 0
    i = index_order[0][0]
    if wabbits[i][1] == 'G':
        pb_tot_tab[i][0] *= frac(0,4)
        pb_tot_tab[i][1] *= frac(0,2)
        pb_tot_tab[i][2] *= frac(1,4)
    elif wabbits[i][1] == '?':
        pb_tot_tab[i][0] *= frac(1,4)
        pb_tot_tab[i][1] *= frac(1,2)
        pb_tot_tab[i][2] *= frac(1,4)
    else:
        pb_tot_tab[i][0] *= frac(1,4)
        pb_tot_tab[i][1] *= frac(1,2)
        pb_tot_tab[i][2] *= frac(0,4)
    return (rst_tab[0][0]*pb_tot_tab[0][0]+rst_tab[0][1]*pb_tot_tab[0][1]+rst_tab[0][2]*pb_tot_tab[0][2])/(pb_tot_tab[0][0]+pb_tot_tab[0][1]+pb_tot_tab[0][2])


def solution(wabbits, p_numerator, p_denominator):
    pb = frac(p_numerator,p_denominator)
    rst = str(proba_dvt(wabbits,pb)).split('/')
    if len(rst)>1:
        return rst[0]+rst[1]
    return rst[0]+'1'