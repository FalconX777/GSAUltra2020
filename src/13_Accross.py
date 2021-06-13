
import math

def solution(targets,c=1e-3,eps=1e-3,lr=1e-1,epoch_max=10000):
    X = [targets[i][0] for i in range(len(targets))]
    G = [math.sqrt(targets[i][1])+1 for i in range(len(targets))]
        
    def grad_f(X,G,c):        
        gradX = [0 for _ in X]
        gradG = [0 for _ in G]
        
        temp = [0 for _ in targets]
        for i in range(len(X)):
            for j in range(len(targets)):
                temp[j] += max(G[i]**2-abs(X[i]-targets[j][0]),0)
        
        for i in range(len(gradX)):
            for j in range(len(targets)):
                if targets[j][1]-temp[j]<=0:
                    gradX[i] += -c*(G[i]**2>=abs(X[i]-targets[j][0]))*((X[i]>=targets[j][0])-(X[i]<=targets[j][0]))/(targets[j][1]-temp[j])**2
                else:
                    gradX[i] = c*(G[i]**2>=abs(X[i]-targets[j][0]))*((X[i]>=targets[j][0])-(X[i]<=targets[j][0]))/(targets[j][1]-temp[j])**2*10
                    break
        
        for i in range(len(gradG)):
            for j in range(len(targets)):
                if targets[j][1]-temp[j]<=0:
                    gradG[i] += c*(G[i]**2>=abs(X[i]-targets[j][0]))/(targets[j][1]-temp[j])**2
                else:
                    gradG[i] = -c*(G[i]**2>=abs(X[i]-targets[j][0]))*10
                    break
            gradG[i] *= 2*G[i]
            gradG[i] += 2*G[i]
        return gradX,gradG
    
    count = 0
    newX = X
    newG = G
    grad_norm = eps + 1
    rst_min = 0
    for g in G:
        rst_min += g**2
    while grad_norm >= eps and count <= epoch_max:
        acceptable = True
        temp = [0 for _ in targets]
        for i in range(len(newX)):
            for j in range(len(targets)):
                temp[j] += max(newG[i]**2-abs(newX[i]-targets[j][0]),0)
            if targets[j][1]-temp[j]>0:
                acceptable = False
                i = len(newX)
                break

        if acceptable:
            X = newX
            G = newG
            rst = 0
            for g in G:
                rst += g**2
            rst_min = min(rst,rst_min)
        else:
            for i in range(len(G)):
                G[i] += eps
        
        gradX,gradG = grad_f(X,G,c)
        grad_norm = 0
        
        newX = X.copy()
        newG = G.copy()
        
        for i in range(len(X)):
            newX[i] -= gradX[i]*lr
            newG[i] -= gradG[i]*lr
            grad_norm += abs(gradX[i]) + abs(gradG[i])
        count += 1

    return rst_min