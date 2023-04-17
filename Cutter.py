import os
import SearchAlgorithms
import FileOperations
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-c", "--current", default="", help="current directory")
    parser.add_argument("-d", "--destination", default="", help="destination directory")
    parser.add_argument("-f", "--filename", default="", help="name of the file you want to cut down")
    parser.add_argument("-l", "--length", default=3, type=int, help="length parameter, corresponds to depth of search")
    parser.add_argument("-o", "--operation", default="C", help="the type of cutting operation you are performing")
    args = vars(parser.parse_args())    

    current_dir = args["current"]
    destination_dir = args["destination"]
    filename = args["filename"]
    depth = args["length"]
    operation = args["operation"]

    f_curr = os.path.join(current_dir,filename)
    f_dest = os.path.join(destination_dir,filename)
    grids = FileOperations.load_grids(f_curr)
    if len(grids)==1:
        FileOperations.save_grids(grids,f_dest)
    else:
        match operation:
            case "C":
                reduced_grids = grids - SearchAlgorithms.bidirectional_search(grids, depth)
            case "CD":
                reduced_grids = grids - SearchAlgorithms.bidirectional_search_find_destabilizable(grids, depth)
            case "CS":
                reduced_grids = grids - SearchAlgorithms.bidirectional_search_with_stabilization(grids, depth)
            case "D":
                reduced_grids = grids - SearchAlgorithms.find_destabilizable_only(grids, depth)
            case "CSS":
                reduced_grids = grids - SearchAlgorithms.bidirectional_search_with_stabilization_twice(grids, depth)
        if len(reduced_grids)!=0:
            FileOperations.save_grids(reduced_grids,f_dest)
