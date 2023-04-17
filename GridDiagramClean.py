import numpy as np

class GridDiagram:

    # Initializes the grid diagram
    def __init__(self,X,O,label="unlabeled"):
        self.X = np.array(X)+0.5
        self.O = np.array(O)+0.5
        self.n = len(X)

        self.l = 0
        heights = set(np.arange(0,len(X),1))
        while len(heights)!=0:
            self.l += 1
            starting_height = heights.pop()
            curr_height = O[X.index(starting_height)]
            while curr_height != starting_height:
                heights.remove(curr_height)
                curr_height = O[X.index(curr_height)]
        
        self.tb = int(0.5*(self.Maslov_O(self.x_minus())+self.Maslov_O(self.x_plus())))-1
        self.r = int(0.5*(self.Maslov_O(self.x_minus())-self.Maslov_O(self.x_plus())))
        self.label = label
    
    # Internal functions to help calculate the gradings of states
    def I(self,P,Q):
        count = 0
        for q_idx in range(self.n-1):
            for p_idx in range(q_idx+1,self.n):
                if P[p_idx]>Q[q_idx]:
                    count += 1
        return count
    def I_mod(self,P,Q):
        count = 0
        for q_idx in range(self.n):
            for p_idx in range(q_idx,self.n):
                if P[p_idx]>Q[q_idx]:
                    count += 1
        return count
    
    # Functions to calculate the gradings of states
    def Maslov_O(self,s):
        return self.I(self.O,self.O) - self.I_mod(self.O,s) - self.I(s,self.O) + self.I(s,s) + 1
    def Maslov_X(self,s):
        return self.I(self.X,self.X) - self.I_mod(self.X,s) - self.I(s,self.X) + self.I(s,s) + 1
    def Alexander(self,s):
        return int(0.5*(self.Maslov_O(s)-self.Maslov_X(s)) - 0.5*(self.n-self.l))

    # Functions that return important grid states as tuples
    def x_plus(self):
        temp = [int((self.X[i]+0.5)%self.n) for i in range(self.n)]
        return tuple([temp[-1]]+temp[0:-1])
    def x_minus(self):
        return tuple((np.array(self.X - 0.5)).astype(int))
    def y_plus(self):
        temp = [int((self.O[i]+0.5)%self.n) for i in range(self.n)]
        return tuple([temp[-1]]+temp[0:-1])
    def y_minus(self):
        return tuple((np.array(self.O - 0.5)).astype(int))

    # Prints the Maslov gradings of a state
    def print_gradings(self,state):
        print("Maslov Grading=" + str(self.Maslov_O(state)) + ", Alexander Grading=" + str(self.Alexander(state)))

    # Calculates the O-blocked, graded differential of a state
    def d(self,state):

        # Sets up the data structure that will store the answer
        ans = dict()
        for i in range(self.n):
            ans[i]=set()

        for left_col_idx in range(self.n):

            # Initializes the height difference
            height_diff = (self.O[left_col_idx]-state[left_col_idx])%self.n
            X_heights = np.zeros(self.n)
            X_heights[
                int((self.X[left_col_idx]-state[left_col_idx])%self.n - 0.5):
                ] += 1

            col_counter = 1
            while (col_counter<self.n and height_diff>1):
                right_col_idx = (left_col_idx + col_counter)%self.n

                # Determines if the rectangle is valid
                if (state[right_col_idx]-state[left_col_idx])%self.n < height_diff:                
                    newstate = list(state)
                    newstate[right_col_idx] = state[left_col_idx]
                    newstate[left_col_idx] = state[right_col_idx]
                    newstate = tuple(newstate)

                    # Labeling the arrow, with addition mod 2
                    X_count = X_heights[(state[right_col_idx]-state[left_col_idx])%self.n - 1]
                    if newstate in ans[X_count]:
                        ans[X_count].remove(newstate)
                    else:
                        ans[X_count].add(newstate)

                # Adjusts the height difference and calculates the number of X's per height
                height_diff = min(
                    height_diff,
                    (state[right_col_idx]-state[left_col_idx])%self.n,
                    (self.O[right_col_idx]-state[left_col_idx])%self.n
                )
                X_heights[
                    int((self.X[right_col_idx]-state[left_col_idx]%self.n)-0.5):
                ] += 1

                col_counter += 1
            
        return ans
    
    # Calculates the inverse image of the O-blocked, graded diffferential
    def d_inv(self,state):

        # Sets up the data structure that will store the answer
        ans = dict()
        for i in range(self.n):
            ans[i]=set()
        state = tuple(state)

        for left_col_idx in range(self.n):

            # Initializes the height difference
            height_diff = (state[left_col_idx]-self.O[left_col_idx])%self.n
            X_heights = np.zeros(self.n)
            X_heights[
                int((state[left_col_idx]-self.X[left_col_idx])%self.n - 0.5):
                ] += 1
            
            col_counter = 1
            while (col_counter<self.n and height_diff>1):
            
                right_col_idx = (left_col_idx + col_counter)%self.n

                # Determines if the rectangle is valid
                if (state[left_col_idx]-state[right_col_idx])%self.n < height_diff:                
                    newstate = list(state)
                    newstate[right_col_idx] = state[left_col_idx]
                    newstate[left_col_idx] = state[right_col_idx]
                    newstate = tuple(newstate)

                    # Labeling the arrow, with addition mod 2
                    X_count = X_heights[(state[left_col_idx]-state[right_col_idx])%self.n - 1]
                    if newstate in ans[X_count]:
                        ans[X_count].remove(newstate)
                    else:
                        ans[X_count].add(newstate)
                
                # Adjusts the height difference and calculates the number of X's per height
                height_diff = min(
                    height_diff,
                    (state[left_col_idx]-state[right_col_idx])%self.n,
                    (state[left_col_idx]-self.O[right_col_idx])%self.n
                )
                X_heights[
                    int((state[left_col_idx]-self.X[right_col_idx])%self.n-0.5):
                ] += 1

                col_counter += 1

        return ans

    # Finds the set of crossings and returns them as a set of tuples
    def get_crossings(self):

        # Initializes data structures
        Xs,Os = tuple((self.X-0.5).astype(int)),tuple((self.O-0.5).astype(int))
        grid = []
        for i in range(self.n):
            grid.append([])
            for j in range(self.n):
                grid[i].append(set())
        initial_row, initial_col = Xs[0],0
        row,col = Xs[0],0
        vertical = True

        # Traces the path through the grid diagram; the brute force approach
        while True:
            if vertical:
                while row!=Os[col]:
                    if Os[col]>row:
                        grid[row][col].add("U")
                        row += 1
                    else:
                        grid[row][col].add("D")
                        row -= 1
                vertical = False
            else:
                while col != Xs.index(row):
                    if Xs.index(row)>col:
                        grid[row][col].add("R")
                        col += 1
                    else:
                        grid[row][col].add("L")
                        col -= 1
                vertical = True   
            if row==initial_row and col==initial_col:
                break
        
        # Checks each square of the grid diagram for a crossing
        pos_crossings, neg_crossings = set(),set()
        for r in range(self.n):
            for c in range(self.n):
                if grid[r][c]=={'R','D'} or grid[r][c]=={'L','U'}:
                    neg_crossings.add((r,c))
                elif grid[r][c]=={'R','U'} or grid[r][c]=={'L','D'}:
                    pos_crossings.add((r,c))
        
        # Returns the set of positive and negative crossings, unioned together
        return pos_crossings.union(neg_crossings)

    def add_clasp(self,crossing):

         # Initializes data structures
        row,col = crossing
        cX,cO=np.zeros(self.n+4),np.zeros(self.n+4)
        oX,oO = tuple((self.X-0.5).astype(int)), tuple((self.O-0.5).astype(int))

        # Depending on the type of clasp, finds the new Xs and Os

        # X's are S,L
        if oX[col]<oO[col] and oX.index(row)<oO.index(row):
            for c in range(self.n):
                if c<col:
                    if oX[c]<row:
                        cX[c]=oX[c]
                    elif oX[c]==row:
                        cX[c]=oX[c]+3
                    elif oX[c]>row:
                        cX[c]=oX[c]+4

                    if oO[c]<row:
                        cO[c]=oO[c]
                    elif oO[c]==row:
                        cO[c]=oO[c]+4
                    elif oO[c]>row:
                        cO[c]=oO[c]+4

                elif c==col:
                    cX[col] = oX[col]
                    cX[col+1] = row
                    cX[col+2] = row+4
                    cX[col+3] = row+2
                    cX[col+4] = row+1

                    cO[col] = row+2
                    cO[col+1] = oO[col]+4
                    cO[col+2] = row+1
                    cO[col+3] = row
                    cO[col+4] = row+3

                elif c>col:
                    if oX[c]<row:
                        cX[c+4]=oX[c]
                    elif oX[c]==row:
                        cX[c+4]=oX[c]+4
                    elif oX[c]>row:
                        cX[c+4]=oX[c]+4

                    if oO[c]<row:
                        cO[c+4]=oO[c]
                    elif oO[c]==row:
                        cO[c+4]=oO[c]+4
                    elif oO[c]>row:
                        cO[c+4]=oO[c]+4
                
        # X's are S,R
        if oX[col]<oO[col] and oX.index(row)>oO.index(row):
            for c in range(self.n):
                if c<col:
                    if oX[c]<row:
                        cX[c]=oX[c]
                    elif oX[c]==row:
                        cX[c]=oX[c]+4
                    elif oX[c]>row:
                        cX[c]=oX[c]+4

                    if oO[c]<row:
                        cO[c]=oO[c]
                    elif oO[c]==row:
                        cO[c]=oO[c]+3
                    elif oO[c]>row:
                        cO[c]=oO[c]+4

                elif c==col:
                    cX[col] = oX[col]
                    cX[col+1] = row
                    cX[col+2] = row+1
                    cX[col+3] = row+2
                    cX[col+4] = row+3

                    cO[col] = row+2
                    cO[col+1] = oO[col]+4
                    cO[col+2] = row+4
                    cO[col+3] = row
                    cO[col+4] = row+1

                elif c>col:
                    if oX[c]<row:
                        cX[c+4]=oX[c]
                    elif oX[c]==row:
                        cX[c+4]=oX[c]+4
                    elif oX[c]>row:
                        cX[c+4]=oX[c]+4

                    if oO[c]<row:
                        cO[c+4]=oO[c]
                    elif oO[c]==row:
                        cO[c+4]=oO[c]+4
                    elif oO[c]>row:
                        cO[c+4]=oO[c]+4

        # X's are N,L
        if oX[col]>oO[col] and oX.index(row)<oO.index(row):
            for c in range(self.n):
                if c<col:
                    if oX[c]<row:
                        cX[c]=oX[c]
                    elif oX[c]==row:
                        cX[c]=oX[c]+3
                    elif oX[c]>row:
                        cX[c]=oX[c]+4

                    if oO[c]<row:
                        cO[c]=oO[c]
                    elif oO[c]==row:
                        cO[c]=oO[c]+4
                    elif oO[c]>row:
                        cO[c]=oO[c]+4

                elif c==col:
                    cX[col] = row+2
                    cX[col+1] = oX[col]+4
                    cX[col+2] = row+4
                    cX[col+3] = row
                    cX[col+4] = row+1

                    cO[col] = oO[col]
                    cO[col+1] = row
                    cO[col+2] = row+1
                    cO[col+3] = row+2
                    cO[col+4] = row+3

                elif c>col:
                    if oX[c]<row:
                        cX[c+4]=oX[c]
                    elif oX[c]==row:
                        cX[c+4]=oX[c]+4
                    elif oX[c]>row:
                        cX[c+4]=oX[c]+4

                    if oO[c]<row:
                        cO[c+4]=oO[c]
                    elif oO[c]==row:
                        cO[c+4]=oO[c]+4
                    elif oO[c]>row:
                        cO[c+4]=oO[c]+4

        # X's are N,R
        if oX[col]>oO[col] and oX.index(row)>oO.index(row):
            for c in range(self.n):
                if c<col:
                    if oX[c]<row:
                        cX[c]=oX[c]
                    elif oX[c]==row:
                        cX[c]=oX[c]+4
                    elif oX[c]>row:
                        cX[c]=oX[c]+4

                    if oO[c]<row:
                        cO[c]=oO[c]
                    elif oO[c]==row:
                        cO[c]=oO[c]+3
                    elif oO[c]>row:
                        cO[c]=oO[c]+4

                elif c==col:
                    cX[col] = row+2
                    cX[col+1] = oX[col]+4
                    cX[col+2] = row+1
                    cX[col+3] = row
                    cX[col+4] = row+3

                    cO[col] = oO[col]
                    cO[col+1] = row
                    cO[col+2] = row+4
                    cO[col+3] = row+2
                    cO[col+4] = row+1

                elif c>col:
                    if oX[c]<row:
                        cX[c+4]=oX[c]
                    elif oX[c]==row:
                        cX[c+4]=oX[c]+4
                    elif oX[c]>row:
                        cX[c+4]=oX[c]+4

                    if oO[c]<row:
                        cO[c+4]=oO[c]
                    elif oO[c]==row:
                        cO[c+4]=oO[c]+4
                    elif oO[c]>row:
                        cO[c+4]=oO[c]+4
        
        return GridDiagram(
            tuple(cX.astype(int)),
            tuple(cO.astype(int)),
            self.label+" with clasp at " + str(crossing))

    def reverse(self):
        revX = [int(self.O[i]-0.5) for i in range(self.n)]
        revO = [int(self.X[i]-0.5) for i in range(self.n)]
        return GridDiagram(revX,revO,self.label)
    def leg_mirror(self):
        rotX = [self.n-int(self.X[self.n-i-1]-0.5)-1 for i in range(self.n)]
        rotO = [self.n-int(self.O[self.n-i-1]-0.5)-1 for i in range(self.n)]
        return GridDiagram(rotX,rotO,self.label)

    def __str__(self):
        return self.label+": "+str(tuple((self.X-0.5).astype(int)))+", "+str(tuple((self.O-0.5).astype(int)))

