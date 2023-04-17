import numpy as np
import itertools

# From Algorithm X, needs citation
def solve(X, Y, solution=[]):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()
def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols
def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)

# Generates the set of valid x-permutations, and the set of valid o-permutations that go with it
def generate_valid_x_perms(n):
    valid_x_perms = set()
    temp = list(itertools.permutations(tuple(range(1,n))))
    for permutation in temp:
        valid_x_perms.add(tuple([0]+list(permutation)))
    for x_perm in valid_x_perms.copy():
        if x_perm in valid_x_perms:
            for j in range(1,n):
                y = tuple([(x_perm[(i+j)%n]-x_perm[j])%n for i in range(n)])
                if y in valid_x_perms and y!=x_perm:
                    valid_x_perms.remove(y)
    return valid_x_perms
def generate_valid_o_perms(x_perm):
    n = len(x_perm)
    # Some internal functions
    def blocked_matrix():
        mat = np.ones((n,n),int)
        for i in range(n):
            mat[x_perm[i],i] = False
            mat[x_perm[i],(i-1)%n] = False
            mat[x_perm[i],(i+1)%n] = False
            mat[(x_perm[i]-1)%n,i] = False
            mat[(x_perm[i]+1)%n,i] = False
        return mat
    def constraint_matrix(blocked_matrix):
        constraint_matrix = []
        for row in range(len(blocked_matrix)):
            for col in range(len(blocked_matrix[row])):
                if blocked_matrix[row][col]:
                    constraint_matrix.append([0]*(1+2*len(blocked_matrix)))
                    constraint_matrix[-1][0] = n*row + col
                    constraint_matrix[-1][1+row] = 1
                    constraint_matrix[-1][1+len(blocked_matrix)+col] = 1
        return constraint_matrix
    def XY(constraint_matrix):
        # generates the X-dict by reading down the columns
        X = dict()
        for col in range(1,len(constraint_matrix[0])):
            X[col-1] = set()
            for row in range(len(constraint_matrix)):
                if constraint_matrix[row][col]:
                    X[col-1].add(constraint_matrix[row][0])
        
        # generates the Y-dict by reading across the rows
        Y = dict()
        for row in range(len(constraint_matrix)):
            grid_square = constraint_matrix[row][0]
            Y[grid_square] = [
                grid_square//n,
                grid_square%n + n
            ]

        return X,Y
    def to_permutation(O_set):
        O_perm = [0]*n
        for grid_square in O_set:
            O_perm[grid_square%n] = grid_square//n
        return tuple(O_perm)
    
    # Actually executes what we want
    o_perms = set()
    B=blocked_matrix()
    C=constraint_matrix(B)
    X,Y = XY(C)
    for o_set in solve(X,Y):
        o_perms.add(to_permutation(o_set))
    return o_perms
def is_knot(grid):
    X,O,n = grid[0],grid[1],len(grid[0])
    heights = set(np.arange(0,n,1))
    curr_height = O[X.index(0)]
    while curr_height!=0:
        heights.remove(curr_height)
        curr_height = O[X.index(curr_height)]
    return len(heights)==1

    
