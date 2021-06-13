# Version submitted

def solution(ps):
    ps = [sorted(ps[i]) for i in range(len(ps))]
    d = [[[0 for _ in range(len(ps[i]))] for _ in range(10)] for i in range(len(ps))]
    d_max = 10*len(ps)+1
    for p in range(10):
        for j in range(len(d[-1][p])):
            d[-1][p][j] = p+1
    for i in range(len(d)-2,-1,-1):
        for p in range(10):
            for j in range(len(d[i][p])):
                # d_min initialization
                d_min = d_max
                
                # d_min computing
                for j_ in range(0,len(d[i+1][p])): # optimisation possible pour trouver le j_min qui convient par dichotomie
                    if ps[i+1][j_]>=ps[i][j]-5:
                        if ps[i+1][j_]>=ps[i][j]+6:
                            break
                        if ps[i+1][j_]<ps[i][j]:
                            d_min = min(d_min,d[i+1][max(p-1,0)][j_])
                        elif ps[i+1][j_]==ps[i][j]:
                            d_min = min(d_min,d[i+1][p][j_])
                        else:
                            d_min = min(d_min,d[i+1][min(p+1,9)][j_])
                
                # updating d
                d[i][p][j] = p+1 + d_min    
    return min(d[0][4][:])