import GridMoves
import GridDiagram
import pickle
import time

LOUD_MODE = False



# Input: a grid G and an integer depth d
# Output: the set of grids that are related to G by a sequence of up to d commutations and/or cyclic permutations

def find_equiv_grids(grid,depth):
    equiv_grids, last_layer = {grid}, {grid}
    for d in range(depth):
        new_grids = set()
        for grid in last_layer:
            #switch!!!!
            for cyclic_equiv_grid in GridMoves.generate_cyclic_equivalent_grids(grid):
                for commut_equiv_grid in GridMoves.generate_commutation_equivalent_grids(cyclic_equiv_grid):
                    if commut_equiv_grid not in equiv_grids:
                        new_grids.add(commut_equiv_grid)
        equiv_grids = equiv_grids.union(new_grids)
        last_layer = new_grids
        if len(new_grids)==0:
            return equiv_grids
        del new_grids
    return equiv_grids


# Input: a set S of grids and a depth d
# Output: a subset T of S that contains grids which are either 
        # a) detabilizable, or
        # b) are asotopic to a grid in S - T
        
# Looks for destabilizable grids (grids with a length-one segment) 
# by generating an equivalence neighborhood of given depth for each grid,
# but also looks for grids isotopic to the above, by checking if neighborhoods intrersect.
# This captures grids that may need 2(depth) moves to get to a form with a short segment.
# Quadratic in size of grids set.

def bidirectional_search_find_destabilizable(grids,depth):
    
    # creates a dictionary whose keys are the grids from the argument, 
    # and value for each key is a set of grids equivalent to it.
    # at this stage, all this is in memory, but for size 10 it was not a concern
    # sorts the original list of grids by size of the discovered equivalence set.
    
    grids_dict = dict()
    for grid in grids:
        grids_dict[grid]=find_equiv_grids(grid,depth)
    grids_list = list(grids)
    grids_list.sort(key=lambda grid:len(grids_dict[grid]))
    if LOUD_MODE:
        for grid in grids_list:
            print(len(grids_dict[grid]))

    # for each original grid G, goes through its equivalence set (starts with small sets).
    # if it finds a destibilizable G' equivalent to G, 
    # it adds G to the set destabilizable_grids   

    destabilizable_grids = set()
    for i in range(len(grids_list)):
        for grid in grids_dict[grids_list[i]]:
            if GridMoves.destabilizable(grid):
                if LOUD_MODE:
                    print(f"Destabilizable: {grids_list[i]}")
                destabilizable_grids.add(grids_list[i])
                break
    
    # isotopy_equivalent_grids will be a set S of grids not known to be destabilizable, 
    # but known to have isotopy class representatives in original set minus S.
    
    # For each pair of original grids Gi and Gj with overlapping equivalence classes:
    # If one was already in destabilizable list and the other not, add the other too
    # If neither was in destabilizable list, add Gj to isotopy_equiv_grids
    
    # We return the set T of grids found to be either detabilizable or to have
    # an isotopy class representative remaining in the original set of grids minus T.
    
    isotopy_equiv_grids = set()
    for i in range(len(grids_list)-1):
        for j in range(i+1,len(grids_list)):
            if len(grids_dict[grids_list[i]].intersection(grids_dict[grids_list[j]])) != 0:
                
                
                ###
                ### FOR NOAH, PLEASE ADDRESS AND DELETE:
                ###
        
                # is it faster to check (a) if an element is in a small set, or (b) two larger sets overlap?
                # I think (a), so I'd move the if below to right above the above line. 
                # This way we only check for isotopic grids if both are not already destabilizable.
                # I know once we ge to here, everything is quick, I wonder what the time difference is for like 1 mil grids.
                # based on what I ran, this does seem to matter a lot:
                # 23k grids about 1-2 hrs, 60k grids about 10 hrs, 100k grids over 20 hrs. 
                
                if grids_list[i] in destabilizable_grids and grids_list[j] in destabilizable_grids:
                    pass
                if grids_list[i] in destabilizable_grids and grids_list[j] not in destabilizable_grids:
                    destabilizable_grids.add(grids_list[i])
                    if LOUD_MODE:
                        print(f"Destabilizable: {grids_list[i]} via {grids_list[j]}")
                elif grids_list[j] in destabilizable_grids and grids_list[i] not in destabilizable_grids:
                    destabilizable_grids.add(grids_list[i])
                    if LOUD_MODE:
                        print(f"Destabilizable: {grids_list[i]} via {grids_list[j]}")
                elif grids_list[j] not in isotopy_equiv_grids:
                    isotopy_equiv_grids.add(grids_list[j])
                    G1 = GridDiagram.GridDiagram(grids_list[i][0],grids_list[i][1])
                    G2 = GridDiagram.GridDiagram(grids_list[j][0],grids_list[j][1])
                    if LOUD_MODE:
                        print(f"Isotopy: {grids_list[i]} --> {grids_list[j]}, with ({G1.tb},{G1.r}) --> ({G2.tb},{G2.r})")

    del grids_dict, grids_list
    if LOUD_MODE:
        print(f"Destab number: {len(destabilizable_grids)}")
        print(f"Isotopy number: {len(isotopy_equiv_grids)}")    
    return destabilizable_grids.union(isotopy_equiv_grids)


# Input: a set S of grids and a depth d
# Output: a subset T of S that consists of grids which are asotopic to a grid in S - T

# For each G in S, generates the "neighborhood" of grids that are related to G by a sequence of up to d commutations and/or cyclic permutations. 
# For pairs of grids in S-T, checks if their neighborhoods overlap. If so, the two grids are equivalent, so one is added to T.

def bidirectional_search(grids,depth):
    grids_dict = dict()
    for grid in grids:
        grids_dict[grid]=find_equiv_grids(grid,depth)    
    grids_list = list(grids)
    grids_list.sort(key=lambda grid:len(grids_dict[grid]))
    if LOUD_MODE:
        for grid in grids_list:
            print(len(grids_dict[grid]))
        
    isotopy_equiv_grids = set()
    for i in range(len(grids_list)-1):
        for j in range(i+1,len(grids_list)):
            if j in isotopy_equiv_grids:
                pass
            elif len(grids_dict[grids_list[i]].intersection(grids_dict[grids_list[j]]))!=0:
                isotopy_equiv_grids.add(grids_list[j])
                G1 = GridDiagram.GridDiagram(grids_list[i][0],grids_list[i][1])
                G2 = GridDiagram.GridDiagram(grids_list[j][0],grids_list[j][1])
                if LOUD_MODE:
                    print(f"Isotopy: {grids_list[i]} --> {grids_list[j]}, with ({G1.tb},{G1.r}) --> ({G2.tb},{G2.r})")
    
    del grids_dict, grids_list
    if LOUD_MODE:
        print(f"Isotopy number: {len(isotopy_equiv_grids)}")
    return isotopy_equiv_grids

# Input: a set S of grids and a depth d
# Output: a subset T of S that consists of grids which are asotopic to a grid in S - T

# For each G in S, generates the "neighborhood" of grids that are related to G by a sequence of up to d+1 moves,
# where the first move is a stabilization (Legendrian isotopy), the rest commutations and/or cyclic permutations. 
# For pairs of grids in S-T, checks if their neighborhoods overlap. If so, the two grids are equivalent, so one is added to T.

def bidirectional_search_with_stabilization(grids,depth):
    grids_dict = dict()
    for grid in grids:
        grids_dict[grid]=set()
        for stabilized_grid in GridMoves.generate_stabilized_grids(grid):
            grids_dict[grid] = grids_dict[grid].union(find_equiv_grids(stabilized_grid,depth))    
    grids_list = list(grids)
    grids_list.sort(key=lambda grid:len(grids_dict[grid]))
    if LOUD_MODE:
        for grid in grids_list:
            print(len(grids_dict[grid]))
    
    isotopy_equiv_grids = set()
    for i in range(len(grids_list)-1):
        for j in range(i+1,len(grids_list)):
            if j in isotopy_equiv_grids:
                pass
            elif len(grids_dict[grids_list[i]].intersection(grids_dict[grids_list[j]]))!=0:
                isotopy_equiv_grids.add(grids_list[j])
                G1 = GridDiagram.GridDiagram(grids_list[i][0],grids_list[i][1])
                G2 = GridDiagram.GridDiagram(grids_list[j][0],grids_list[j][1])
                if LOUD_MODE:
                    print(f"Isotopy: {grids_list[i]} --> {grids_list[j]}, with ({G1.tb},{G1.r}) --> ({G2.tb},{G2.r})")

    del grids_dict, grids_list
    if LOUD_MODE:
        print(f"Isotopy number: {len(isotopy_equiv_grids)}")
    return isotopy_equiv_grids

# I think this is NOT a bidirectional search. I'd change the name. 

# Looks for destabilizable grids (grids with a length-one segment) 
# by generating an equivalence neighborhood of given depth for each grid.
# This captures grids that need up to depth-many moves to get to a form with a short segment.
# Linear in size of grids set.

def bidirectional_search_find_destabilizable_only(grids,depth):
    grids_dict = dict()
    for grid in grids:
        grids_dict[grid]=find_equiv_grids(grid,depth)
    grids_list = list(grids)
    grids_list.sort(key=lambda grid:len(grids_dict[grid]))
    if LOUD_MODE:
        for grid in grids_list:
            print(len(grids_dict[grid]))

    destabilizable_grids = set()
    for i in range(len(grids_list)):
        for grid in grids_dict[grids_list[i]]:
            if GridMoves.destabilizable(grid):
                if LOUD_MODE:
                    print(f"Destabilizable: {grids_list[i]}")
                destabilizable_grids.add(grids_list[i])
                break
    
    del grids_dict, grids_list
    if LOUD_MODE:
        print(f"Destab number: {len(destabilizable_grids)}")
    return destabilizable_grids

if __name__=='__main__':

    X=(0,1,2,6,4,5,3)
    O=(2,4,3,0,6,1,5)
    g = (X,O)
    find_equiv_grids(g,100)

    with open("Remaining_Grids_Bucketed/RemainingPairs_tb=-10_r=-3.txt",'rb') as f:
        grids = pickle.load(f)
    f.close()
    with open("Remaining_Grids_Bucketed/RemainingPairs_tb=-7_r=-2.txt",'rb') as f:
        grids2 = pickle.load(f)
    f.close()
    half = set()
    count = 0
    for g in grids:
        count += 1
        if count<10000:
            half.add(g)
    for g in grids2:
        half.add(g)
    print(len(half))
    time.sleep(3)
    for depth in range(1,10):
        half = half - bidirectional_search_find_destabilizable(half,depth)
        print(len(half))
        time.sleep(5)
    for depth in range(1,6):
        half = half-bidirectional_search_with_stabilization(half,depth)
        print(len(half))
        time.sleep(5)

