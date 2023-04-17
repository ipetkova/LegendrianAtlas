# import snappy
import subprocess

def trace(X,O):
    dir = 'UP'
    loc = [0,1]
    locations = [(0,0)]
    
    locations_dict = dict()
    locations_dict[(0,0)]=[]
    locations_dict[(0,0)].append({"IN":"LEFT","OUT":"UP"})

    while loc!=[0,0]:
        locations.append(tuple(loc))
        if tuple(loc) not in locations_dict.keys():
            locations_dict[tuple(loc)] = []
        locations_dict[tuple(loc)].append({"IN":dir})

        if X[loc[0]]==loc[1]:
            if O[loc[0]]<loc[1]:
                dir = 'DOWN'
            else:
                dir = 'UP'
        if O[loc[0]]==loc[1]:
            if X.index(loc[1])>loc[0]:
                dir = 'RIGHT'
            else:
                dir = 'LEFT'
        
        locations_dict[tuple(loc)][-1]["OUT"] = dir
        
        match dir:
            case 'UP':
                loc[1] += 1
            case 'DOWN':
                loc[1] -= 1
            case 'RIGHT':
                loc[0] += 1
            case 'LEFT':
                loc[0] -= 1
        
    return locations, locations_dict
def label_strands_for_PD_code(locations, location_info):
    intersections = set()
    labeled_strands = dict()
    curr_strand = 0

    for loc in location_info.keys():
        labeled_strands[loc]=[]
        if len(location_info[loc])==2:
            intersections.add(loc)
    
    visited = set()
    for loc in locations:
        t = 1*(loc in visited)
        visited.add(loc)
        curr_info = location_info[loc][t]
        if loc not in intersections:
            labeled_strands[loc].append({
                    'IN':[curr_info['IN'],curr_strand],
                    'OUT':[curr_info['OUT'],curr_strand]
                })
        else:
            labeled_strands[loc].append({
                    'IN':[curr_info['IN'],curr_strand],
                    'OUT':[curr_info['IN'],(curr_strand+1)%(2*len(intersections))]
                })
            curr_strand = (curr_strand+1)%(2*len(intersections))

    intersection_info = dict()
    for loc in intersections:
        t = 1*(labeled_strands[loc][0]['IN'][0]=='LEFT' or labeled_strands[loc][0]['IN'][0]=='RIGHT')
        intersection_info[loc] = {
            'TOP-IN': labeled_strands[loc][t]['IN'][1],
            'TOP-OUT': labeled_strands[loc][t]['OUT'][1],
            'BOTTOM-IN': labeled_strands[loc][not t]['IN'][1],
            'BOTTOM-OUT': labeled_strands[loc][not t]['OUT'][1]
        }
        if {labeled_strands[loc][0]['IN'][0],labeled_strands[loc][1]['IN'][0]}=={'UP','LEFT'} or {labeled_strands[loc][0]['IN'][0],labeled_strands[loc][1]['IN'][0]}=={'DOWN','RIGHT'}:
            intersection_info[loc]['ORIENTATION'] = 'POSITIVE'
        else:
            intersection_info[loc]['ORIENTATION'] = 'NEGATIVE'

    return intersection_info    
def gen_PD_code(intersection_info):
    PD_code = []
    for intersection in intersection_info.keys():
        if intersection_info[intersection]['ORIENTATION']=='POSITIVE':
            PD_code.append([
                intersection_info[intersection]['BOTTOM-IN'],
                intersection_info[intersection]['TOP-OUT'],
                intersection_info[intersection]['BOTTOM-OUT'],
                intersection_info[intersection]['TOP-IN']
                ])
        elif intersection_info[intersection]['ORIENTATION']=='NEGATIVE':
            PD_code.append([
                intersection_info[intersection]['BOTTOM-IN'],
                intersection_info[intersection]['TOP-IN'],
                intersection_info[intersection]['BOTTOM-OUT'],
                intersection_info[intersection]['TOP-OUT']          
                ])
    return PD_code
def PD_code(grid):
    X,O = grid[0],grid[1]
    locations, location_info = trace(X,O)
    intersection_info = label_strands_for_PD_code(locations, location_info)
    return gen_PD_code(intersection_info)   
def get_knot_type(grid):
    pd = PD_code(grid)
    L = snappy.Link(pd)
    return L.exterior().identify()

def get_alexander_polynomial(grid):
    X,O = grid[0],grid[1]
    space = " "
    args = f"-x {space.join(str(i) for i in X)} -o {space.join(str(i) for i in O)}"
    cmd = f"sage AlexanderPolynomialCalculator.sage {args}"
    print(subprocess.check_output(cmd,shell=True))

if __name__ == '__main__':
    get_alexander_polynomial(((0,1,2,3,4),(2,3,4,0,1)))
    get_alexander_polynomial(((0,1,2,3,4),(2,3,4,0,1)))
    get_alexander_polynomial(((0,1,2,3,4),(2,3,4,0,1)))
    get_alexander_polynomial(((0,1,2,3,4),(2,3,4,0,1)))
    get_alexander_polynomial(((0,1,2,3,4),(2,3,4,0,1)))
    get_alexander_polynomial(((0,1,2,3,4),(2,3,4,0,1)))
    print("done")
