# Version submitted

def center(pos1,pos2):
    pos = []
    for k in range(len(pos1)):
        pos += [(pos1[k]+pos2[k])//2]
    return pos
def dist(pos1,pos2):
    d = 0
    for k in range(len(pos1)):
        d += (pos1[k]-pos2[k])**2
    return d

def solution(masses, locations): 
    zipped_lists = zip(masses, locations)
    sorted_pairs = sorted(zipped_lists)
    tuples = zip(*sorted_pairs)
    masses,locations = [list(tuple) for tuple in tuples]
    
    while len(masses)>1:    
        d = [dist(locations[0],locations[i]) for i in range(1,len(locations))]
        i_min = 1
        for i in range(len(d)):
            if d[i_min-1]>d[i]:
                i_min = i+1
        masses[i_min] += masses[0]
        locations[i_min] = center(locations[i_min],locations[0])
        masses = masses[1:]
        locations = locations[1:]
        
        j = i_min-1
        while j < len(masses)-1 and masses[j] > masses[j+1]:  # Partial bubble sort 
            masses[j], masses[j+1] = masses[j+1], masses[j] 
            locations[j], locations[j+1] = locations[j+1], locations[j] 
            j += 1
    rst = 0
    for k in range(len(locations[0])):
        rst += locations[0][k]
    return rst