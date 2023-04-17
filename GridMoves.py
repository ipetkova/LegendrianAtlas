# A library for all the grid moves
# Standard input is a grid, output is a set of grids
# including some extra code for speed testing

from itertools import permutations
import pickle
import time


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
    X,O,n,new_grids = grid[0],grid[1],len(grid[0]),set()
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

def generate_pinched_grids(grid):
    X,O,n, new_grids = grid[0],grid[1],len(grid[0]),set()
    for i in range(n-1):
        if (X[i]-1==X[i+1]) and (O[i]!=X[i]-1) and (O[i+1]!=X[i+1]+1):
            j=X[i]
            if (O.index(j+1)<i and O.index(j)>(i+1))==(O[i]<j and O[i+1]>(j+1)):
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


def legendrian_destabilizable(grid):
    X,O,n = grid[0],grid[1],len(grid[0])
    
    for col in range(n):
        x_height,o_height = X[col],O[col]
        x_idx, o_idx = X.index(o_height), O.index(x_height)
        if x_height>o_height:
            if x_idx<col and (o_idx<x_idx or o_idx>col):
                start,end = x_idx,col
                destabilizable = True
                for col2 in range(start+1,end):
                    destabilizable = (X[col2]<x_height and X[col2]>o_height) == (O[col2]<x_height and O[col2]>o_height)
                    if not destabilizable:
                        break
                if destabilizable:
                    return True
            
            if o_idx>col and (x_idx>o_idx or x_idx>col):
                start,end = col,o_idx
                destabilizable = True
                for col2 in range(start+1,end):
                    destabilizable = (X[col2]<x_height and X[col2]>o_height) == (O[col2]<x_height and O[col2]>o_height)
                    if not destabilizable:
                        break
                if destabilizable:
                    return True
        
        if o_height>x_height:
            if x_idx>col and (o_idx>x_idx or o_idx<col):
                start,end = col,x_idx
                destabilizable = True
                for col2 in range(start+1,end):
                    destabilizable = (X[col2]<o_height and X[col2]>x_height) == (O[col2]<o_height and O[col2]>x_height)
                    if not destabilizable:
                        break
                if destabilizable:
                    return True
            
            if o_idx<col and (x_idx<o_idx or x_idx>col):
                start,end = o_idx,col
                destabilizable = True
                for col2 in range(start+1,end):
                    destabilizable = (X[col2]<o_height and X[col2]>x_height) == (O[col2]<o_height and O[col2]>x_height)
                    if not destabilizable:
                        break
                if destabilizable:
                    return True
    
    for row in range(n):
        x_idx, o_idx = X.index(row), O.index(row)
        x_height, o_height = X[o_idx], O[x_idx]

        if x_idx<o_idx:
            if x_height>row and (o_height>x_height or o_height<row):
                start,end = row,x_height
                destabilizable = True
                for row2 in range(start+1,end):
                    destabilizable = (X.index(row2)>x_idx and X.index(row2)<o_idx)==(O.index(row2)>x_idx and O.index(row2)<o_idx)
                    if not destabilizable:
                        break
                if destabilizable:
                    return True
            
            if o_height<row and (x_height<o_height or x_height>row):
                start,end = o_height,row
                destabilizable = True
                for row2 in range(start+1,end):
                    destabilizable = (X.index(row2)>x_idx and X.index(row2)<o_idx)==(O.index(row2)>x_idx and O.index(row2)<o_idx)
                    if not destabilizable:
                        break
                if destabilizable:
                    return True
        
        if o_idx<x_idx:
            if x_height<row and (o_height<x_height or o_height>row):
                start,end = x_height,row
                destabilizable = True
                for row2 in range(start+1,end):
                    destabilizable = (X.index(row2)>o_idx and X.index(row2)<x_idx)==(O.index(row2)>o_idx and O.index(row2)<x_idx)
                    if not destabilizable:
                        break
                if destabilizable:
                    return True
            
            if o_height>row and (x_height>o_height or x_height<row):
                start,end = row,o_height
                destabilizable = True
                for row2 in range(start+1,end):
                    destabilizable = (X.index(row2)>o_idx and X.index(row2)<x_idx)==(O.index(row2)>o_idx and O.index(row2)<x_idx)
                    if not destabilizable:
                        break
                if destabilizable:
                    return True
    
    return False

if __name__=='__main__':
    with open("RemainingGrids_01_18",'rb') as f:
        grids = pickle.load(f)
    f.close()
    to = time.time()
    for grid in grids:
        generate_cyclic_equivalent_grids(grid)
    print(time.time()-to)