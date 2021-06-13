def esp_gain_b_dvt(r,d,sa,vals,dice_vals,db_gain_b,p_dict_tab): # sa = sum_Alice
    # Base case
    s = 0
    for v in vals:
        s += v
    if r == 1:
        db_gain_b[str([r,sa,vals])] = [(s>sa)-(s<sa),0]
        return None
    # Recursion
    d_max = 0
    g_max = db_gain_b[str([r-1,sa,vals])][0]
    d_down = 0
    while d_down<len(vals) and vals[d_down] == dice_vals[0]:
        d_down += 1
    d_up = d
    while d_up>0 and vals[d_up-1] == dice_vals[-1]:
        d_up -= 1
    for d_loc in range(max(1,d_down),d_up+1): # on bankera tjs les (d-d_loc) meilleurs dés
        g_loc = 0
        c = 0
        for key,w in p_dict_tab[d_loc].items():
            vals_loc = w[1]
            vals_loc = vals_loc + vals[d_loc:]
            vals_loc = sorted(vals_loc)
            g_loc += w[0]*db_gain_b[str([r-1,sa,vals_loc])][0]
            c += w[0]
        g_loc /= c
        if g_loc > g_max:
            g_max = g_loc
            d_max = d_loc
    # Improve db
    db_gain_b[str([r,sa,vals])] = [g_max,d_max]
    # Result
    return None

def gain_b_dvt(r,d,sa,dice_vals,db_gain_b,db_gain_b_sa,p_dict_tab):
    esp_rst = 0
    for key,w in p_dict_tab[d].items():
        vals = w[1]
        esp_rst += w[0]*db_gain_b[str([r,sa,vals])][0]
    esp_rst /= len(dice_vals)**d
    db_gain_b_sa[str(sa)] = esp_rst
    return esp_rst

def esp_gain_a_dvt(r,d,vals,dice_vals,db_gain_a,db_gain_b_sa,p_dict_tab):
    # Base case
    s = 0
    for v in vals:
        s += v
    if r == 1:
        db_gain_a[str([r,vals])] = [-db_gain_b_sa[str(s)],0]
        return [-db_gain_b_sa[str(s)],0]
    # Recursion
    d_max = 0
    g_max = db_gain_a[str([r-1,vals])][0]
    d_down = 0
    while d_down<len(vals) and vals[d_down] == dice_vals[0]:
        d_down += 1
    d_up = d
    while d_up>0 and vals[d_up-1] == dice_vals[-1]:
        d_up -= 1
    for d_loc in range(max(1,d_down),d_up+1): # on bankera tjs les (d-d_loc) meilleurs dés
        g_loc = 0
        c = 0
        for key,w in p_dict_tab[d_loc].items():
            vals_loc = w[1]
            vals_loc = vals_loc + vals[d_loc:]
            vals_loc = sorted(vals_loc)
            g_loc += w[0]*db_gain_a[str([r-1,vals_loc])][0]
            c += w[0]
        g_loc /= c
        if g_loc > g_max:
            g_max = g_loc
            d_max = d_loc
    # Improve db
    db_gain_a[str([r,vals])] = [g_max,d_max]
    # Result
    return g_max,d_max

def proba_dvt(r,d,dice_vals,db_gain_a,p_dict_tab):
    db_pb_tab = [dict() for _ in range(r+1)]
    # r_loc = r
    db_pb = db_pb_tab[r]
    for key,w in p_dict_tab[d].items():
        vals_loc = w[1]
        db_pb[str(vals_loc)] = w[0]/len(dice_vals)**d
    # r_loc < r
    for r_loc in range(r-1,-1,-1):
        db_pb = db_pb_tab[r_loc]
        for key,value in db_pb_tab[r_loc+1].items():
            vals = key[1:-1].split(', ')
            for i in range(len(vals)):
                vals[i] = int(vals[i])
            g_loc,d_loc = db_gain_a[str([r_loc+1,vals])]
            
            if d_loc == 0:
                rst = db_pb.get(str(vals))
                if rst != None:
                    db_pb[str(vals)] += value/len(dice_vals)**d_loc
                else:
                    db_pb[str(vals)] = value/len(dice_vals)**d_loc
            else:
                for keyp,w in p_dict_tab[d_loc].items():
                    vals_loc = w[1]
                    vals_loc = vals_loc + vals[d_loc:]
                    vals_loc = sorted(vals_loc)
                    rst = db_pb.get(str(vals_loc))
                    if rst != None:
                        db_pb[str(vals_loc)] += w[0]*value/len(dice_vals)**d_loc
                    else:
                        db_pb[str(vals_loc)] = w[0]*value/len(dice_vals)**d_loc
    # pb_sum
    db_sum = dict()
    for key,value in db_pb_tab[0].items():
        vals = key[1:-1].split(', ')
        for i in range(len(vals)):
            vals[i] = int(vals[i])
        s = 0
        for v in vals:
            s += v
        rst = db_sum.get(str(s))
        if rst != None:
            db_sum[str(s)] += value
        else:
            db_sum[str(s)] = value
    return db_sum

def solution(dice_vals,d,r):
    dice_vals = sorted(dice_vals)
    # parcours building
    p_dict_tab = [dict() for _ in range(d+1)]
    for d_loc in range(1,d+1):
        count = [0 for _ in range(d_loc)]
        conti = True
        while conti:
            vals = [dice_vals[count[i]] for i in range(len(count))]
            vals = sorted(vals)
            rst = p_dict_tab[d_loc].get(str(vals))
            if rst == None:
                p_dict_tab[d_loc][str(vals)] = [1,vals]
            else:
                p_dict_tab[d_loc][str(vals)][0] += 1
            conti = False
            for i in range(len(count)-1,-1,-1):
                count[i] = (count[i]+1)%len(dice_vals)
                if count[i] != 0:
                    conti = True
                    break
    # sa_tab building
    sa_dict = dict()
    for key,w in p_dict_tab[d].items():
        vals = w[1]
        s = 0
        for v in vals:
            s += v
        sa_dict[str(s)] = True
    # esp_gain_b building
    db_gain_b = dict()
    for key,value in sa_dict.items():
        sa = int(key)
        for r_loc in range(1,r+1):
            for key,w in p_dict_tab[d].items():
                vals = w[1]
                esp_gain_b_dvt(r_loc,d,sa,vals,dice_vals,db_gain_b,p_dict_tab)
    # db_gain_b_sa building
    db_gain_b_sa = dict()
    for key,value in sa_dict.items():
        sa = int(key)
        gain_b_dvt(r,d,sa,dice_vals,db_gain_b,db_gain_b_sa,p_dict_tab)
    # db_esp_a building
    db_gain_a = dict()
    for r_loc in range(1,r+1):
        for key,w in p_dict_tab[d].items():
            vals = w[1]
            esp_gain_a_dvt(r_loc,d,vals,dice_vals,db_gain_a,db_gain_b_sa,p_dict_tab)
    # db_pb_sum_a building
    db_pb_sum_a = proba_dvt(r,d,dice_vals,db_gain_a,p_dict_tab)
    # esp_rst computing
    esp_rst = 0
    for key,value in db_pb_sum_a.items():
        sa = int(key)
        for keyp,w in p_dict_tab[d].items():
            vals = w[1]
            esp_rst += w[0]*value*db_gain_b[str([r,sa,vals])][0]/len(dice_vals)**d
    return ("%.7f" % esp_rst)[2:]