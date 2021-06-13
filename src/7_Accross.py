def solution(a, m):
    db = [2]
    for _ in range(2203):
        db += [(db[-1]**2)%m]
    # db[i] = 2**(2**i)%m
    rst = 0
    for x in a:
        while x>m:
            x = x%m + x//m
        loc_rst = 1
        i = 0
        while (x > 0):
            if ((x & 1) > 0):
                loc_rst = (loc_rst*db[i])%m
            x = x>>1
            i += 1
        rst = (rst+loc_rst)
    return rst%m