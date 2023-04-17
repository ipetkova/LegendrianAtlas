import sage
import os
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import FileOperations

def get_alexander_polynomial(grid):
    X,O,n = grid[0],grid[1],len(grid[0])
    R.<t> = PolynomialRing(ZZ, 't')

    mat = [[0]*(n+1) for i in range(n+1)]
    for r in range(n+1):
        mat[r][0] = 1
        for c in range(1,n+1):
            if X[c-1]<r and O[c-1]>=r:
                mat[r][c] = mat[r][c-1]*t
            elif X[c-1]>=r and O[c-1]<r:
                mat[r][c] = mat[r][c-1]*(t**-1)
            else:
                mat[r][c] = mat[r][c-1]
    del mat[0]
    for row in mat:
        del row[-1]

    M = Matrix(mat)

    A_pol = M.determinant()
    #at this point, due to negative powers of t, A_pol has become a fraction field element
    
    if A_pol == 0:
        return (0,)
    else:
        #account for grid size by dividing by a power of 1-t
        A_pol = A_pol / ((1-t)^(n-1))
        #valuation returns the lowest degree of the poly
        min_deg = A_pol.valuation()
        #normalize to go from free term to 2deg
        A_pol = A_pol*(t^(-min_deg))
        #cast in R, was fraction field element
        A_pol = R(A_pol)
        #reflect if leading=constant coefficient is negative
        if A_pol.constant_coefficient() < 1:
            A_pol = - A_pol
        #extract coefficients
        A_coeffs = A_pol.list()
        return tuple(A_coeffs)

if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-c", "--current", default="", help="the current directory")
    parser.add_argument("-d", "--destination", default="", help="the destination directory")
    parser.add_argument("-f", "--filename", default="", help="the filename containing grids to be calculated")
    args = vars(parser.parse_args())    

    curr_dir = args["current"]
    dest_dir = args["destination"]
    filename = args["filename"]
    
    pols_dict = dict()
    pathname = os.path.join(curr_dir,filename)
    grids = FileOperations.load_grids(pathname)
    if len(grids)>0:
        for grid in grids:
            pol = get_alexander_polynomial(grid)
            if pol not in pols_dict.keys():
                pols_dict[pol] = set()
            pols_dict[pol].add(grid)
    for pol in pols_dict.keys():
        pol_str=str(pol)[1:-1].replace(" ","")
        if pol_str[-1]==',':
            pol_str=pol_str[:-1]
        new_filename = f"{filename}_A={pol_str}"
        FileOperations.save_grids(pols_dict[pol],os.path.join(dest_dir,new_filename))