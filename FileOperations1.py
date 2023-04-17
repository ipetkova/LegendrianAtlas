import pickle
import os
import GridGenerator
import GridDiagram
import SearchAlgorithms

def save_grids(grids, filename):
    with open(filename,'wb') as f:
        pickle.dump(grids,f)
    f.close()
def load_grids(filename):
    with open(filename,'rb') as f:
        grids = pickle.load(f)
    f.close()
#    for grid in grids:
#        print(grid)
    return grids

def create_initial_files(grid_size, location):
    os.system(f'cd {location}')
    os.system('mkdir InitialGrids')

    x_perms = GridGenerator.generate_valid_x_perms(grid_size)
    count = 0
    for X in x_perms:
        grids = set()
        for O in GridGenerator.generate_valid_o_perms(X):
            grid = (X,O)
            if GridGenerator.is_knot(grid):
                grids.add(grid)
        name = ''.join([str(X[i]) for i in range(len(X))])
        pathname = f"InitialGrids/{name}"
        save_grids(grids,pathname)
        count += 100
        print(count/len(x_perms))

def reduce_buckets_short_segments(location, curr_dir, dest_dir, depth):
    os.system(f"cd {location}")
    os.system(f"mkdir {dest_dir}")
    for filename in os.listdir(curr_dir):
        f = os.path.join(curr_dir,filename)
        if os.path.isfile(f):
            os.system(
                f"nohup python3 Cutter.py " + \
                f"-c {curr_dir} " + \
                f"-d {dest_dir} " + \
                f"-f {filename} " + \
                f"-l {depth} " + \
                f"-o CD &"
            )
def reduce_buckets(location, curr_dir, dest_dir, depth):
    os.system(f"cd {location}")
    os.system(f"mkdir {dest_dir}")
    for filename in os.listdir(curr_dir):
        f = os.path.join(curr_dir,filename)
        if os.path.isfile(f):
            os.system(
                f"nohup python3 Cutter.py " + \
                f"-c {curr_dir} " + \
                f"-d {dest_dir} " + \
                f"-f {filename} " + \
                f"-l {depth} " + \
                f"-o C &"
            )
def reduce_buckets_with_stab(location, curr_dir, dest_dir, depth):
    os.system(f"cd {location}")
    os.system(f"mkdir {dest_dir}")
    for filename in os.listdir(curr_dir):
        f = os.path.join(curr_dir,filename)
        if os.path.isfile(f):
            os.system(
                f"nohup python3 Cutter.py " + \
                f"-c {curr_dir} " + \
                f"-d {dest_dir} " + \
                f"-f {filename} " + \
                f"-l {depth} " + \
                f"-o CS &"
            )

def reduce_buckets_short_segments_only(location, curr_dir, dest_dir, depth):
    os.system(f"cd {location}")
    for filename in os.listdir(curr_dir):
        f = os.path.join(curr_dir,filename)
        if os.path.isfile(f):
            os.system(
                f"nohup python3 Cutter2.py " + \
                f"-c {curr_dir} " + \
                f"-d {dest_dir} " + \
                f"-f {filename} " + \
                f"-l {depth} " + \
                f"-o D &"
            )

def reduce_buckets_short_segments_temp(location, curr_dir, dest_dir, depth):
    os.system(f"cd {location}")
    for filename in os.listdir(curr_dir):
        f = os.path.join(curr_dir,filename)
        if os.path.isfile(f) and filename not in os.listdir(dest_dir):
            os.system(
                f"nohup python3 Cutter2.py " + \
                f"-c {curr_dir} " + \
                f"-d {dest_dir} " + \
                f"-f {filename} " + \
                f"-l {depth} " + \
                f"-o CD &"
            )

def mainline_reduce_buckets_short_segments(location, curr_dir, dest_dir, depth):
    os.system(f"cd {location}")
    os.system(f"mkdir {dest_dir}")
    count = 0
    for filename in os.listdir(curr_dir):
        f = os.path.join(curr_dir,filename)
        if os.path.isfile(f):
            count += 1
            grids = load_grids(f)
            print(len(grids))
            grids = grids-SearchAlgorithms.bidirectional_search_find_destabilizable(grids,depth)
            print(len(grids))
            print()
            save_grids(grids,f)
            if count%100 == 0:
                print(count)

def get_statistics(location, foldername):
    num_buckets, tot_grids = 0,0

    os.system(f"cd {location}")
    for filename in os.listdir(foldername):
        f = os.path.join(foldername,filename)
        if os.path.isfile(f):
            g = load_grids(f)
            num_buckets += 1
            tot_grids += len(g)
            if num_buckets%100==0:
                print(num_buckets)
    print(f"{num_buckets} buckets, {tot_grids} total grids")

def rebucket_by_tb_r(location, curr_dir, dest_dir):
    os.system(f"cd {location}")
    os.system(f"mkdir {dest_dir}")
    
    # creates an empty file for each (tb,r) in the range.
    for tb in range(-25,25):
        for r in range(-25,25):
            filename = f"tb={tb}_r={r}"
            pathname = os.path.join(dest_dir,filename)
            save_grids(set(),pathname)
    
    # creates a dictionary with one key for each (tb,r) in the range, and empty set values.
    sorting_dict = dict()
    for tb in range(-25,25):
        for r in range(-25,25):
            key = (tb,r)
            sorting_dict[key] = set()

    # goes through files in the current directory
    # for each file
        # loads grids (pairs of perms) from it 
        # turns each grid into grid diagram G
        # adds grid to dictionary, with key its own (tb(G), r(G))
        
        # for each (tb,r) cut-pastes content for that key from dictionary to that file. 
        
        # the idea is that dictionary is kept relatively small at each step, filled only with content for the current perm file.
            
    for filename in os.listdir(curr_dir):
        f = os.path.join(curr_dir,filename)
        if os.path.isfile(f):
            grids = load_grids(f)
            for grid in grids:
                G = GridDiagramClean.GridDiagram(grid[0],grid[1])
                key = (G.tb,G.r)
                sorting_dict[key].add(grid)
        for tb in range(-25,25):
            for r in range(-25,25):
                filename=f"tb={tb}_r={r}"
                pathname = os.path.join(dest_dir,filename)
                temp = load_grids(pathname)
                # above will currently be mepty. 
                # below key will be the last value from the previous cycle and will never change to match tb,r.
                # fix: replace "key" with "(tb,r)"
                key = (tb,r)
                temp = temp.union(sorting_dict[key])
                save_grids(temp, pathname)
                sorting_dict[key] = set()
    
    # eliminates resulting files that are empty.
    
    for tb in range(-25,25):
        for r in range(-25,25):
            filename = f"tb={tb}_r={r}"
            pathname = os.path.join(dest_dir,filename)
            grids = load_grids(pathname)
            if len(grids)==0:
                os.system(f"rm {pathname}")


def rebucket_small_buckets(location, curr_dir, dest_dir):
    os.system(f"cd {location}")
    os.system(f"mkdir {dest_dir}")
    for filename in os.listdir(curr_dir):
        old_pathname = os.path.join(curr_dir,filename)
        if os.path.isfile(old_pathname):
            grids = load_grids(old_pathname)
            if len(grids)>1000:
                count, num_buckets = 0, 0
                temp_bucket = set()
                for grid in grids:
                    count += 1
                    temp_bucket.add(grid)
                    if count%1000==0:
                        num_buckets += 1
                        new_pathname = f"{os.path.join(dest_dir,filename)}_bucket{num_buckets}"
                        save_grids(temp_bucket, new_pathname)
                        temp_bucket = set()
                if len(temp_bucket)>0:
                    num_buckets += 1
                    new_pathname = f"{os.path.join(dest_dir,filename)}_bucket{num_buckets}"
                    save_grids(temp_bucket, new_pathname)
            else:
                new_pathname = os.path.join(dest_dir,filename)
                save_grids(grids, new_pathname)

def rebucket_by_alexPoly_topType(location, curr_dir, dest_dir):
    os.system(f"cd {curr_dir}")
    os.system(f"mkdir {dest_dir}")


def recombine_small_buckets(location, curr_dir, dest_dir):
    os.system(f"cd {location}")
    os.system(f"mkdir {dest_dir}")
    for filename in sorted(list(os.listdir(curr_dir))):
        pathname = os.path.join(curr_dir,filename)
        if os.path.isfile(pathname):
            filename_arr = filename.split('_')
            if len(filename_arr)==3:
                new_filename = f"{filename_arr[0]}_{filename_arr[1]}"
                new_pathname = os.path.join(dest_dir,new_filename)
                if os.path.isfile(new_pathname):
                    grids = load_grids(new_pathname)
                    grids = grids.union(load_grids(pathname))
                    save_grids(grids, new_pathname)
                else:
                    save_grids(grids, new_pathname)
            else:
                new_pathname = os.path.join(dest_dir, filename)
                grids = load_grids(pathname)
                save_grids(grids, new_pathname)




if __name__=='__main__':
    #get_statistics("~/Desktop/Projects/FilteredGRID","InitialGrids")
    #get_statistics("generate_size_9","size_9_tb_r")
    #create_initial_files(9, 'size_9')
    #rebucket_by_tb_r('generate_size_9', 'InitialGrids', 'size_9_tb_r')
    #reduce_buckets_short_segments("generate_size_9", "size_9_tb_r_no_short_16", "size_9_tb_r_no_short_20", 20)
    reduce_buckets_with_stab("generate_size_9", "size_9_tb_r_no_short_20", "size_9_tb_r_no_short_20_stab_12", 12)
