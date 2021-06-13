def solution(n, proposition):
    proposition = proposition.lower()
    new_prop = ''
    for i in range(len(proposition)):
        if proposition[i] == '(':
            new_prop += '( '
        elif proposition[i] == ')':
            new_prop += ' )'
        else:
            new_prop += proposition[i]
    rst = 0
    var_set = 'abcdefghijklmnopqrstuvwxyz'
    var_set = var_set[:n]
    loop = [[False,True] for _ in var_set]
    count = [0 for _ in var_set]
    loc_prep = new_prop.split(' ')
    while True:
        eva_prep = ''
        for j in range(len(loc_prep)):
            if len(loc_prep[j]) == 1:
                try:
                    var_ind = var_set.index(loc_prep[j])
                    eva_prep += str(count[var_ind]==1)+' '
                except ValueError:
                    eva_prep += loc_prep[j]+' '
            else:
                 eva_prep += loc_prep[j]+' '
        rst += eval(eva_prep)
        for i in range(len(count)-1,-1,-1):
            count[i] = (count[i]+1)%2
            if count[i]%2 == 1:
                break
        if i == 0 and count[0]%2 == 0:
            break
    return rst