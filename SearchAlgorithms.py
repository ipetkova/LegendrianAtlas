import GridMoves
import pickle
import time


def find_equiv_grids(grids,depth):
    equiv_grids, last_layer = grids.copy(), grids.copy()
    for d in range(depth):
        new_grids = set()
        for grid in last_layer:
            for commut_equiv_grid in GridMoves.generate_commutation_equivalent_grids(grid):
                for cyclic_equiv_grid in GridMoves.generate_cyclic_equivalent_grids(commut_equiv_grid):
                    if cyclic_equiv_grid not in equiv_grids:
                        new_grids.add(cyclic_equiv_grid)
        equiv_grids = equiv_grids.union(new_grids)
        last_layer = new_grids
        if len(new_grids)==0:
            return equiv_grids
        del new_grids
    return equiv_grids

def bidirectional_search_find_destabilizable(grids,depth):
    grids_dict = dict()
    for grid in grids:
        grids_dict[grid]=find_equiv_grids({grid},depth)
    grids_list = list(grids)
    grids_list.sort(key=lambda grid:len(grids_dict[grid]))
    
    destabilizable_grids = set()
    for i in range(len(grids_list)):
        for grid in grids_dict[grids_list[i]]:
            if GridMoves.destabilizable(grid):
                destabilizable_grids.add(grids_list[i])
                break
        
    isotopy_equiv_grids = set()
    for i in range(len(grids_list)-1):
        for j in range(i+1,len(grids_list)):
            if len(grids_dict[grids_list[i]].intersection(grids_dict[grids_list[j]])) != 0:
                if grids_list[i] in destabilizable_grids and grids_list[j] in destabilizable_grids:
                    pass
                if grids_list[i] in destabilizable_grids and grids_list[j] not in destabilizable_grids:
                    destabilizable_grids.add(grids_list[i])
                elif grids_list[j] in destabilizable_grids and grids_list[i] not in destabilizable_grids:
                    destabilizable_grids.add(grids_list[i])
                elif grids_list[j] not in isotopy_equiv_grids:
                    isotopy_equiv_grids.add(grids_list[j])

    del grids_dict, grids_list
    return destabilizable_grids.union(isotopy_equiv_grids)

def bidirectional_search(grids,depth):
    grids_dict = dict()
    for grid in grids:
        grids_dict[grid]=find_equiv_grids({grid},depth)    
    grids_list = list(grids)
    grids_list.sort(key=lambda grid:len(grids_dict[grid]))
        
    isotopy_equiv_grids = set()
    for i in range(len(grids_list)-1):
        for j in range(i+1,len(grids_list)):
            if j in isotopy_equiv_grids:
                pass
            elif len(grids_dict[grids_list[i]].intersection(grids_dict[grids_list[j]]))!=0:
                isotopy_equiv_grids.add(grids_list[j])
    
    del grids_dict, grids_list
    return isotopy_equiv_grids

def bidirectional_search_with_stabilization(grids,depth):
    grids_dict = dict()
    for grid in grids:
        grids_dict[grid]=set()
        for stabilized_grid in GridMoves.generate_stabilized_grids(grid):
            grids_dict[grid] = grids_dict[grid].union(find_equiv_grids({stabilized_grid},depth))    
    grids_list = list(grids)
    grids_list.sort(key=lambda grid:len(grids_dict[grid]))
    
    isotopy_equiv_grids = set()
    for i in range(len(grids_list)-1):
        for j in range(i+1,len(grids_list)):
            if j in isotopy_equiv_grids:
                pass
            elif len(grids_dict[grids_list[i]].intersection(grids_dict[grids_list[j]]))!=0:
                isotopy_equiv_grids.add(grids_list[j])

    del grids_dict, grids_list
    return isotopy_equiv_grids


def bidirectional_search_with_stabilization_twice(grids,depth):
    grids_dict = dict()
    for grid in grids:
        grids_dict[grid]=set()
        temp = set()
        for stabilized_grid in GridMoves.generate_stabilized_grids(grid):
            for stabilized_grid_2 in GridMoves.generate_stabilized_grids(stabilized_grid):
                temp.add(stabilized_grid_2)
        grids_dict[grid]=find_equiv_grids(temp,depth)
    grids_list = list(grids)
    grids_list.sort(key=lambda grid:len(grids_dict[grid]))
    
    isotopy_equiv_grids = set()
    for i in range(len(grids_list)-1):
        for j in range(i+1,len(grids_list)):
            if j in isotopy_equiv_grids:
                pass
            elif len(grids_dict[grids_list[i]].intersection(grids_dict[grids_list[j]]))!=0:
                isotopy_equiv_grids.add(grids_list[j])

    del grids_dict, grids_list
    return isotopy_equiv_grids


def bidirectional_search_find_destabilizable_only(grids,depth):
    grids_dict = dict()
    for grid in grids:
        grids_dict[grid]=find_equiv_grids({grid},depth)
    grids_list = list(grids)
    grids_list.sort(key=lambda grid:len(grids_dict[grid]))

    destabilizable_grids = set()
    for i in range(len(grids_list)):
        for grid in grids_dict[grids_list[i]]:
            if GridMoves.destabilizable(grid):
                destabilizable_grids.add(grids_list[i])
                break
    
    del grids_dict, grids_list
    return destabilizable_grids


def find_legendrian_destabilizable_only(grids):
    destabilizable_grids = set()
    for grid in grids:
        if GridMoves.legendrian_destabilizable(grid):
            destabilizable_grids.add(grid)
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

