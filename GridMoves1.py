# A library for all the grid moves
# Standard input is a grid, output is a set of grids
# including some extra code for speed testing

from itertools import permutations
import pickle
import time
#import snappy


def generate_cyclic_equivalent_grids(grid):
    X,O,n = grid[0],grid[1],len(grid[0])
    new_grids = set()
    for i in range(n):
        temp_x = [(X[j]-X[i])%n for j in range(n)]
        temp_o = [(O[j]-X[i])%n for j in range(n)]
        temp_x = temp_x[i:n]+temp_x[0:i]
        temp_o = temp_o[i:n]+temp_o[0:i]
        new_grids.add((tuple(temp_x),tuple(temp_o)))
        del temp_x, temp_o
    return new_grids


def commutable (x1,o1,x2,o2):
    nested = (x1 > min(x2,o2) and x1 < max(x2,o2)) and (o1 > min(x2,o2) and o1 < max(x2,o2))
    side_by_side = (x1 < min(x2,o2) and o1 < min(x2,o2)) or (x1 > max(x2,o2) and o1 > max(x2,o2))
    return (nested or side_by_side)
def interleaving(x1,o1,x2,o2):
    x_sandwiched = (x1<o2 and x1>x2) or (x1>o2 and x1<x2)
    o_sandwiched = (o1<x2 and o1>o2) or (o1>x2 and o1<o2)
    return (x_sandwiched^o_sandwiched) or (x1==o2 or o1==x2)
def col_swap(col,X,O):
    X_new = X[:col]+(X[col+1],X[col])+X[col+2:]
    O_new = O[:col]+(O[col+1],O[col])+O[col+2:]
    return X_new, O_new
def row_swap(row,X,O):
    x_idx_row1 = X.index(row)
    x_idx_row2 = X.index(row+1)
    o_idx_row1 = O.index(row)
    o_idx_row2 = O.index(row+1)
    x_idx_1 = min(x_idx_row1,x_idx_row2)
    x_idx_2 = max(x_idx_row1,x_idx_row2)
    o_idx_1 = min(o_idx_row1,o_idx_row2)
    o_idx_2 = max(o_idx_row1,o_idx_row2)
    X_new = X[:x_idx_1] + (row+(1*(x_idx_row1<x_idx_row2)),) + X[x_idx_1+1:x_idx_2] + (row+(1*(x_idx_row1>x_idx_row2)),) + X[x_idx_2+1:]
    O_new = O[:o_idx_1] + (row+(1*(o_idx_row1<o_idx_row2)),) + O[o_idx_1+1:o_idx_2] + (row+(1*(o_idx_row1>o_idx_row2)),) + O[o_idx_2+1:]
    del x_idx_1, x_idx_2, o_idx_1, o_idx_2
    return X_new,O_new
def generate_commutation_equivalent_grids(grid):
    X,O,n,new_grids = grid[0],grid[1],len(grid[0]),{grid}
    for i in range(0,n-1):
        x1, o1 = X[i], O[i]
        x2, o2 = X[i+1], O[i+1]
        if commutable(x1,o1,x2,o2):
            new_grids.add(col_swap(i,X,O))
    for i in range(0,n-1):
        x1, o1 = X.index(i), O.index(i)
        x2, o2 = X.index(i+1), O.index(i+1)
        if commutable(x1,o1,x2,o2):
            new_grids.add(row_swap(i,X,O))
    return new_grids


# Input: a grid, a column, and a type of stabilization (only Legendrian isotopies here)
# Output: the resulting stabilized grid
def stabilize(X,O,col,type):
    n = len(X)
    X_new, O_new = [],[]

    match type:
        case "X:NW":
            height = X[col]
            for c in range(n):
                if c!=col:
                    X_new.append(X[c]+(X[c]>=height))
                    O_new.append(O[c]+(O[c]>=height))
                else:
                    X_new.append(height)
                    O_new.append(O[c]+(O[c]>=height))
                    X_new.append(height+1)
                    O_new.append(height)
        
        case "X:SE":
            height = X[col]
            for c in range(n):
                if c!=col:
                    X_new.append(X[c]+(X[c]>height))
                    O_new.append(O[c]+(O[c]>height))
                else:
                    X_new.append(height)
                    O_new.append(height+1)
                    X_new.append(height+1)
                    O_new.append(O[c]+(O[c]>=height))
        
        case "O:NW":
            height = O[col]
            for c in range(n):
                if c!=col:
                    X_new.append(X[c]+(X[c]>=height))
                    O_new.append(O[c]+(O[c]>=height))
                else:
                    O_new.append(height)
                    X_new.append(X[c]+(X[c]>=height))
                    X_new.append(height)
                    O_new.append(height+1)
        
        case "O:SE":
            height = O[col]
            for c in range(n):
                if c!=col:
                    X_new.append(X[c]+(X[c]>height))
                    O_new.append(O[c]+(O[c]>height))
                else:
                    O_new.append(height)
                    X_new.append(height+1)
                    X_new.append(X[c]+(X[c]>=height))
                    O_new.append(height+1)        
    
    return tuple(X_new),tuple(O_new)

# generates all grids related to the input by a stabilization that is a Legendrian isotopy
def generate_stabilized_grids(grid):
    X,O,n,new_grids = grid[0],grid[1],len(grid[0]),set()
    for i in range(n):
        new_grids.add(stabilize(X,O,i,"X:NW"))
        new_grids.add(stabilize(X,O,i,"X:SE"))
        new_grids.add(stabilize(X,O,i,"O:NW"))
        new_grids.add(stabilize(X,O,i,"O:SE"))
    return new_grids

def generate_destabilized_grids(grid):
    X,O,n,new_grids = grid[0],grid[1],len(grid[0]),set()
    for col in range(n-1):
        if X[col]+1==X[col+1]:
            if (O[col+1]==X[col] and O[col]!=X[col+1]):
                print(f"X:NW,{col}")
                X_new,O_new,row = [],[],X[col]
                for i in range(n-1):
                    X_new.append(X[i+(i>col)]-(X[i+(i>col)]>row))
                    O_new.append(O[i+(i>col)]-(O[i+(i>col)]>row))
            new_grids.add((tuple(X_new),tuple(O_new)))

            if (O[col+1]!=X[col] and O[col]==X[col+1]):
                print(f"X:SE, {col}")
                X_new,O_new,row = [],[],X[col+1]
                for i in range(n-1):
                    X_new.append(X[i+(i>=col)]-(X[i+(i>=col)]>=row))
                    O_new.append(O[i+(i>=col)]-(O[i+(i>=col)]>=row))
            new_grids.add((tuple(X_new),tuple(O_new)))
       
        if O[col]+1==O[col+1]:
            if (X[col+1]==O[col] and X[col]!=O[col+1]):
                print(f"O:NW, {col}")
                X_new, O_new, row = [],[],O[col]
                for i in range(n-1):
                    X_new.append(X[i+(i>col)]-(X[i+(i>col)]>row))
                    O_new.append(O[i+(i>col)]-(O[i+(i>col)]>row))
            new_grids.add((tuple(X_new),tuple(O_new)))

            if (X[col+1]!=O[col] and X[col]==O[col+1]):
                print(f"O:SE, {col}")
                X_new, O_new, row = [],[],O[col+1]
                for i in range(n-1):
                    X_new.append(X[i+(i>=col)]-(X[i+(i>=col)]>=row))
                    O_new.append(O[i+(i>=col)]-(O[i+(i>=col)]>=row))
            new_grids.add((tuple(X_new),tuple(O_new)))
    
    return new_grids  

def destabilizable(grid):
    X,O,n = grid[0],grid[1],len(grid[0])
    for i in range(n):
        if (abs(X[i]-O[i])==1 or abs(X.index(i)-O.index(i)==1)):
            return True
    return False


# A pair of functions to calculate speedily whether two knots are transversely destabilizable
# Positive transverse destabilizable means that performing the destabilization will INCREASE r
def positive_transverse_destabilizable(grid):
    X,O,n = grid[0],grid[1],len(grid[0])
    for col in range(n):
        if (X[col]-O[col])%n==1:
            row = O[col]
            if ((X.index((row+1)%n)-col)%n)>((O.index(row)-col)%n):
                return True
    for row in range(n):
        if (O.index(row)-X.index(row))%n==1:
            col = X.index(row)
            if ((X[(col+1)%n]-row)%n)>((O[col]-row)%n):
                return True
    return False
def negative_transverse_destabilizable(grid):
    X,O,n = grid[0],grid[1],len(grid[0])
    for col in range(n):
        if (O[col]-X[col])%n==1:
            row = X[col]
            if ((X.index((row+1)%n)-col)%n)>((O.index(row)-col)%n):
                return True
    for row in range(n):
        if (O.index(row)-X.index(row))%n == 1:
            col = X.index(row)
            if ((X[(col+1)%n]-row)%n)>((O[col]-row)%n):
                return True
    return False

def generate_pinched_grids(grid):
    X,O,n, new_grids = grid[0],grid[1],len(grid[0]),set()
    for i in range(n-1):
        if (X[i]-1==X[i+1]) and (O[i]!=X[i]-1) and (O[i+1]!=X[i+1]+1):
            j=X[i]
            if (O.index(j)<i and O.index(j-1)>(i+1))==(O[i]<j and O[i+1]>(j+1)):
                new_grids.add((X[:i]+(j-1,j)+X[i+2:],O))
    return new_grids
def generate_depinched_grids(grid):
    X,O,n,new_grids = grid[0],grid[1],len(grid[0]),set()
    for i in range(n-1):
        if (X[i]+1==X[i+1]) and (O[i]!=X[i]+1) and (O[i+1]!=X[i+1]-1):
            j = X[i]
            if (O.index(j+1)<i and O.index(j)>i+1)==(O[i]<j and O[i+1]>j+1):
                new_grids.add((X[:i]+(j+1,j)+X[i+2:],O))
    return new_grids

# A pair of functions that find all the pinches (depinches) possible from a given grid
# Some speedups are implemented here, I can explain them in a writeup?
def pinch(grid):
    X,O = grid[0],grid[1]
    n = len(X)
    new_grids = set()

    # Row pinches
    for i in range(n-1):
        a = O.index(i+1)
        b = X.index(i+1)
        c = X.index(i)
        d = O.index(i)

        if a<b and b<c and c<d:
            if O[b]<i and O[c]>i+1:
                X_new = list(X).copy()
                X_new[b]=i
                X_new[c]=i+1
                new_grids.add((tuple(X_new),O))
        if d<b and b<c and c<a:
            if O[b]>i+1 and O[c]<i:
                X_new = list(X).copy()
                X_new[b]=i
                X_new[c]=i+1
                new_grids.add((tuple(X_new),O))
        if b<a and a<d and d<c:
            if X[a]<i and X[d]>i+1:
                O_new = list(O).copy()
                O_new[a]=i
                O_new[d]=i+1
                new_grids.add((X,tuple(O_new)))
        if c<a and a<d and d<b:
            if X[a]>i+1 and X[d]<i:
                O_new = list(O).copy()
                O_new[a]=i
                O_new[d]=i+1
                new_grids.add((X,tuple(O_new)))
 
    # Col pinches
    for i in range(n-1):
        a = O[i]
        b = X[i+1]
        c = X[i]
        d = O[i+1]

        if a<b and b<c and c<d:
            if O.index(c)<i and O.index(b)>i+1:
                X_new = list(X).copy()
                X_new[i]=b
                X_new[i+1]=c
                new_grids.add((tuple(X_new),O)) 
        if d<b and b<c and c<a:
            if O.index(b)<i and O.index(c)>i+1:
                X_new = list(X).copy()
                X_new[i]=b
                X_new[i+1]=c
                new_grids.add((tuple(X_new),O))
        if c<d and d<a and a<b:
            if X.index(a)<i and X.index(d)>i+1:
                O_new = list(O).copy()
                O_new[i] = d
                O_new[i+1] = a
                new_grids.add((X,tuple(O_new)))
        if b<d and d<a and a<c:
            if X.index(d)<i and X.index(a)>i+1:
                O_new = list(O).copy()
                O_new[i] = d
                O_new[i+1] = a
                new_grids.add((X,tuple(O_new)))
    
    return new_grids
def depinch(grid):
    X,O = grid[0],grid[1]
    n = len(X)
    new_grids = set()

    # Row depinches
    for i in range(n-1):
        a = O.index(i+1)
        b = X.index(i+1)
        c = X.index(i)
        d = O.index(i)

        if a<c and c<b and b<d:
            if O[b]>i+1 and O[c]<i:
                X_new = list(X).copy()
                X_new[b]=i
                X_new[c]=i+1
                new_grids.add((tuple(X_new),O))
        if d<c and c<b and b<a:
            if O[c]>i+1 and O[b]<i:
                X_new = list(X).copy()
                X_new[b]=i
                X_new[c]=i+1
                new_grids.add((tuple(X_new),O))
        if b<d and d<a and a<c:
            if X[d]<i and X[a]>i+1:
                O_new = list(O).copy()
                O_new[d] = i+1
                O_new[a] = i
                new_grids.add((X,tuple(O_new)))
        if c<d and c<a and a<b:
            if X[d]>i+1 and X[a]<i:
                O_new = list(O).copy()
                O_new[d] = i+1
                O_new[a] = i
                new_grids.add((X,tuple(O_new)))

    # Col depinches
    for i in range(n-1):
        a = O[i]
        b = X[i+1]
        c = X[i]
        d = O[i+1]

        if a<c and c<b and b<d:
            if O.index(c)>i+1 and O.index(b)<i:
                X_new = list(X).copy()
                X_new[i] = b
                X_new[i+1] = c
                new_grids.add((tuple(X_new),O))
        if d<c and c<b and b<a:
            if O.index(c)<i and O.index(b)>i+1:
                X_new = list(X).copy()
                X_new[i] = b
                X_new[i+1] = c
                new_grids.add((tuple(X_new),O))
        if c<a and a<d and d<b:
            if X.index(a)>i+1 and X.index(d)<i:
                O_new = list(O).copy()
                O_new[i] = d
                O_new[i+1]= a
                new_grids.add((X,tuple(O_new)))
        if b<a and a<d and d<c:
            if X.index(a)<i and X.index(d)>i+1:
                O_new = list(O).copy()
                O_new[i] = d
                O_new[i+1] = a
                new_grids.add((X,tuple(O_new)))

    return new_grids
    
# A pair of functions that find all the birth (death) moves available from a given grid
# Birth just acts everywhere possible, death finds any possible unknot death given that it is 4 connected vertices,
#  subject to a small speedup condition
def birth(grid):
    X,O = grid[0],grid[1]
    n = len(X)
    new_grids = set()

    for i,j in zip(range(n+1),range(n+1)):
        a,b = i-0.5, j-0.5
        X_new, O_new = [0]*(n+2), [0]*(n+2)
        for c in range(n):
            if c<a:
                X_new[c]=X[c]+2*(X[c]>b)
                O_new[c]=O[c]+2*(O[c]>b)
            else:
                X_new[c+2]=X[c]+2*(X[c]>b)
                O_new[c+2]=O[c]+2*(O[c]>b)

        # For convenience, adds both orientations of the unknot
        # These are Legendrian isotopic, but this just speeds things up a bit
        X_new[i], X_new[i+1]=j,j+1
        O_new[i], O_new[i+1]=j+1,j
        new_grids.add((tuple(X_new),tuple(O_new)))
        X_new[i], X_new[i+1]=j+1,j
        O_new[i], O_new[i+1]=j,j+1
        new_grids.add((tuple(X_new),tuple(O_new)))
    
    return new_grids
def death(grid):
    X,O = grid[0],grid[1]
    n = len(X)
    new_grids = set()

    for i in range(n-1):
        for j in range(i,n):
            if X[i]==O[j] and O[i]==X[j]:
                low, high = min(X[i],X[j]), max(X[i],X[j])

                # check the inside of this box both in rows and columns; can be slightly sped up by breaking loops
                row_check, col_check = True, True
                for r in range(low+1,high):
                    row_check = row_check and (X.index(r)>i and X.index(r)<j)==(O.index(r)>i and O.index(r)<j)
                for c in range(i+1,j):
                    col_check = col_check and (X[c]>low and X[c]<high)==(O[c]>low and O[c]<high)
                
                # if the box is empty, creates the new grid
                if row_check or col_check:
                    X_new, O_new = [0]*(n-2),[0]*(n-2)
                    for c in range(n-2):
                        X_new[c-(c>i)-(c>j)]=X[c]-(X[c]>low)-(X[c]>high)
                        O_new[c-(c>i)-(c>j)]=O[c]-(O[c]>low)-(O[c]>high)
                    new_grids.add((X_new,O_new))
    
    return new_grids



# NEED A BETTER HOME FOR THIS CODE
### Maybe in GridDiagram.py from here till line 541. Also, Ina renamed GridDiagramClean.py to GridDiagram.py. Check if we've edited code in other files accordingly.  
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
    pd = PD_code(grid)
    L = snappy.Link(pd)
    print(L.alexander_polynomial())

if __name__=='__main__':
    with open("RemainingGrids_01_18",'rb') as f:
        grids = pickle.load(f)
    f.close()
    to = time.time()
    print(len(grids))
    for grid in grids:
        pinch(grid)
        depinch(grid)
    print(time.time()-to)
