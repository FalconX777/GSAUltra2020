def solution(a, b):
    if len(a) == 0:
        if len(b) == 0:
            return 0
        rst = abs(b[0])
        for j in range(1,len(b)):
            rst += abs(b[j-1]-b[j])
        return rst
    if len(b) == 0:
        return solution(b,a)
    mat = [[[0,0] for j in range(len(b)+1)] for i in range(len(a)+1)] # [d_min(a[:i],b[:j],last_pos=a[i-1]),...b[j-1]]
    mat[1][0] = [abs(a[0]),abs(a[0])]
    mat[0][1] = [abs(b[0]),abs(b[0])]
    for i in range(2,len(a)+1):
        mat[i][0] = [mat[i-1][0][0]+abs(a[i-1]-a[i-2]),mat[i-1][0][1]+abs(a[i-1]-a[i-2])]
    for j in range(2,len(b)+1):
        mat[0][j] = [mat[0][j-1][1]+abs(b[j-1]-b[j-2]),mat[0][j-1][1]+abs(b[j-1]-b[j-2])]
    
    # Loop
    mat[1][1][0] = mat[0][1][0]+abs(a[0]-b[0])
    mat[1][1][1] = mat[1][0][1]+abs(b[0]-a[0])
    for j in range(2,len(b)+1):
        mat[1][j][0] = mat[0][j][1]+abs(a[0]-b[j-1])
        mat[1][j][1] = min(mat[1][j-1][0]+abs(b[j-1]-a[0]),mat[1][j-1][1]+abs(b[j-1]-b[j-2]))
    
    for i in range(2,len(a)+1):
        mat[i][1][0] = min(mat[i-1][1][0]+abs(a[i-1]-a[i-2]),mat[i-1][1][1]+abs(a[i-1]-b[0]))
        mat[i][1][1] = mat[i][0][0]+abs(b[0]-a[i-1])
        for j in range(2,len(b)+1):
            mat[i][j][0] = min(mat[i-1][j][0]+abs(a[i-1]-a[i-2]),mat[i-1][j][1]+abs(a[i-1]-b[j-1]))
            mat[i][j][1] = min(mat[i][j-1][0]+abs(b[j-1]-a[i-1]),mat[i][j-1][1]+abs(b[j-1]-b[j-2]))
    return min(mat[-1][-1][0],mat[-1][-1][1])