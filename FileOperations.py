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

def reduce_buckets_with_stab_twice(location, curr_dir, dest_dir, depth):
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
                f"-o CSS &"
            )

def reduce_buckets_with_stab_twice_in_series(location, curr_dir, dest_dir, depth):
    os.system(f"cd {location}")
    os.system(f"mkdir {dest_dir}")
    for filename in os.listdir(curr_dir):
        print(filename)
        f_curr = os.path.join(curr_dir,filename)
        f_dest = os.path.join(dest_dir,filename)
        grids = load_grids(f_curr)
        if len(grids)==1:
            save_grids(grids,f_dest)
        else:
            reduced_grids = grids - SearchAlgorithms.bidirectional_search_with_stabilization_twice(grids, depth)
            save_grids(reduced_grids,f_dest)

def reduce_buckets_short_segments_temp(location, curr_dir, dest_dir, depth):
    os.system(f"cd {location}")
    count = 0
    files = list(os.listdir(dest_dir))
    for filename in os.listdir(curr_dir):
        f = os.path.join(curr_dir,filename)
        count += 1
        if count%100==0:
            print(count)
        if os.path.isfile(f) and (filename not in files):
            print("here")
            os.system(
                f"nohup python3 Cutter.py " + \
                f"-c {curr_dir} " + \
                f"-d {dest_dir} " + \
                f"-f {filename} " + \
                f"-l {depth} " + \
                f"-o CD &"
            )

def reduce_buckets_short_segments_only(location, curr_dir, dest_dir, depth):
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
                f"-o D &"
            )

def reduce_buckets_short_segments_legendrian_only(location, curr_dir, dest_dir):
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
                f"-l 0 " + \
                f"-o DL &"
            )

def rebucket_by_tb_r(location, curr_dir, dest_dir):
    os.system(f"cd {location}")
    os.system(f"mkdir {dest_dir}")
    for tb in range(-50,50):
        for r in range(-50,50):
            filename = f"tb={tb}_r={r}"
            pathname = os.path.join(dest_dir,filename)
            save_grids(set(),pathname)
    
    sorting_dict = dict()
    for tb in range(-50,50):
        for r in range(-50,50):
            key = (tb,r)
            sorting_dict[key] = set()

    count = 0
    for filename in os.listdir(curr_dir):
        f = os.path.join(curr_dir,filename)
        if os.path.isfile(f):
            count += 1
            grids = load_grids(f)
            for grid in grids:
                G = GridDiagram.GridDiagram(grid[0],grid[1])
                key = (G.tb,G.r)
                sorting_dict[key].add(grid)
        if count%100==0:
            print(count)

    for tb in range(-50,50):
        for r in range(-50,50):
            filename=f"tb={tb}_r={r}"
            key = (tb,r)
            pathname = os.path.join(dest_dir,filename)
            temp = load_grids(pathname)
            temp = temp.union(sorting_dict[key])
            save_grids(temp, pathname)
            sorting_dict[key] = set()
         
    for tb in range(-50,50):
        for r in range(-50,50):
            filename = f"tb={tb}_r={r}"
            pathname = os.path.join(dest_dir,filename)
            grids = load_grids(pathname)
            if len(grids)==0:
                os.system(f"rm {pathname}")

                
def get_statistics(location, foldername):
    num_buckets, tot_grids = 0,0

    os.system(f"cd {location}")
    for filename in sorted(list(os.listdir(foldername))):
        pathname = os.path.join(foldername,filename)
        if os.path.isfile(pathname):
            g = load_grids(pathname)
            num_buckets += 1
            tot_grids += len(g)
            print(f"bucket {filename}: {len(g)} grids")
    print(f"{num_buckets} buckets, {tot_grids} total grids")

    
def rebucket_small_buckets(location, curr_dir, dest_dir, bucket_size):
    os.system(f"cd {location}")
    os.system(f"mkdir {dest_dir}")
    for filename in os.listdir(curr_dir):
        old_pathname = os.path.join(curr_dir,filename)
        if os.path.isfile(old_pathname):
            grids = load_grids(old_pathname)
            if len(grids)>bucket_size:
                count, num_buckets = 0, 0
                temp_bucket = set()
                for grid in grids:
                    count += 1
                    temp_bucket.add(grid)
                    if count%bucket_size==0:
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
                    grids = load_grids(pathname)
                    save_grids(grids, new_pathname)
            else:
                new_pathname = os.path.join(dest_dir, filename)
                grids = load_grids(pathname)
                save_grids(grids, new_pathname)

def merge_buckets(location, curr_dir, dest_dir):
    os.system(f"cd {location}")
    os.system(f"mkdir {dest_dir}")
    curr_bucket = set()
    count = 0
    for filename in os.listdir(curr_dir):
        pathname = os.path.join(curr_dir,filename)
        if os.path.isfile(pathname):
            count += 1
            curr_bucket = curr_bucket.union(load_grids(pathname))
            if count%50==0:
                save_grids(curr_bucket,os.path.join(dest_dir,str(count)))
                print(count)
                curr_bucket = set()
    if len(curr_bucket)>0:
        save_grids(curr_bucket,os.path.join(dest_dir,str(count)))

def rebucket_by_alexander_polynomial(location, curr_dir, dest_dir):
    os.system(f"cd {location}")
    os.system(f"mkdir {dest_dir}")
    for filename in os.listdir(curr_dir):
        pathname = os.path.join(curr_dir,filename)
        if os.path.isfile(pathname):
            os.system(
                f"nohup sage AlexanderPolynomialCalculator.sage -c {curr_dir} -d {dest_dir} -f {filename} &"
            )

def find_total_cuts(location, dir1, dir2):
    os.system(f"cd {location}")
    total_cut = 0
    for filename in os.listdir(dir2):
        if os.path.isfile(os.path.join(dir2,filename)):
            g1 = load_grids(os.path.join(dir1,filename))
            g2 = load_grids(os.path.join(dir2,filename))
            total_cut += len(g1)-len(g2)
    print(f"total cut: {total_cut}")

    
def yoink_singletons(location, curr_dir, dest_dir):
    os.system(f"cd {location}")
    for filename in os.listdir(curr_dir):
        f_curr = os.path.join(curr_dir,filename)
        grids = load_grids(f_curr)
        if len(grids)==1:
            f_dest = os.path.join(dest_dir,filename)
            save_grids(grids,f_dest)

