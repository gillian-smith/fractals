import numpy as np
from fractals import get_bounds, string_to_list
from PIL import Image
from tqdm import tqdm
import json

def render(params,state):
    calculate(params,state)
    state.result = np.flipud(state.result.T)
    colour(params,state)

def calculate(params,state):
    b = get_bounds(params)
    w = params.width
    h = params.height

    N = params.max_iter # at least 10^5 to see anything good

    # TODO generalise to any size of matrix, any variable entries, any probability distribution
    # 1: start with string/list representation of matrix e.g. [[0,1,1,1,A],[0,0,0,B,0],[1,1,1,0,0],[0,1,1,1,1],[0,1,0,0,0]]
    # 2: read as list using string_to_list
    # 3: on zeroth iter, find indices of any string placeholders e.g. 'A','B' and save them as a list of tuples e.g. [(0,4),(1,3)]
    # 4: replace string placeholders with randomly generated numbers, according to their distribution which is also saved as a string
    #    e.g. '(7+9j)X+(-3-5j)'
    # 5: convert this to a numpy array using np.array(); now we have our matrix
    # 6: on the following iters, use the indices found in step 3 to generate new random values for the appropriate entries of the matrix
    
    M_read, num_placeholders = string_to_list(params.matrix)
    dim = len(M_read) # number of rows and columns (should be the same)

    randoms = np.random.random_sample((N,num_placeholders))
    A = np.empty((N,num_placeholders),dtype=complex)

    dst = params.distribution
    if dst.startswith("uniform"):
        coeffs = [complex(d) for d in dst.removeprefix("uniform ").split(" ")]
        for n in range(len(coeffs)):
            A += coeffs[n] * np.power(randoms,n)

    # find placeholder locations
    # replace placeholders with random numbers from A
    placeholder_locs = []
    for i in range(dim):
        for j in range(dim): # safe bc this should be a square matrix
            if isinstance(M_read[i][j],str):
                placeholder_locs.append((i,j))
                M_read[i][j] = A[0,len(placeholder_locs)-1]

    M = np.array(M_read)
    
    eigenvalues = np.empty(shape=(N,dim), dtype=complex)

    for n in tqdm(range(N)):
        # find eigenvalues
        eigvals = np.linalg.eigvals(M)
        eigenvalues[n,:] = eigvals
        # replace placeholders with new randoms from A
        for ind, loc in enumerate(placeholder_locs):
            M[loc] = A[n,ind]

    eigenvalues = np.reshape(eigenvalues, dim*N)
    x = eigenvalues.real
    y = eigenvalues.imag

    exclude_real_eigenvalues = True
    if exclude_real_eigenvalues:
        number_of_complex_eigenvalues = np.count_nonzero(y)
        x_complex_only = np.empty(number_of_complex_eigenvalues)
        y_complex_only = np.empty(number_of_complex_eigenvalues)
        m = 0
        for n in range(dim*N):
            if y[n]!=0:
                x_complex_only[m] = x[n]
                y_complex_only[m] = y[n]
                m += 1
    else:
        x_complex_only = x
        y_complex_only = y

    state.result,_,_ = np.histogram2d(x_complex_only,y_complex_only,bins=[w,h],range=[[b['xmin'],b['xmax']],[b['ymin'],b['ymax']]],density=False)

def colour(params,state):
    I = state.result
    I = np.power(I,0.5)
    state.img = Image.fromarray(np.uint8(255*(I/np.max(I))))

