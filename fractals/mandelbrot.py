import numpy as np
from fractals import get_bounds
from PIL import Image
from tqdm import tqdm

def render(params,state):
    calculate(params,state)
    state.result = np.flipud(state.result.T)
    colour(params,state)

def calculate(params,state):
    b = get_bounds(params)
    w = params.width
    h = params.height
    x = np.linspace(b['xmin'], b['xmax'], w, endpoint=False, dtype=float)
    y = np.linspace(b['ymin'], b['ymax'], h, endpoint=False, dtype=float)
    X,Y = np.meshgrid(x,y)
    C = X + 1j*Y
    state.result = np.zeros((w,h))
    for i in tqdm(range(w)):
        for j in range(h):
            c = C[j,i]
            in_set, num_iters = in_mandelbrot(c,params.max_iter)
            if not in_set:
                state.result[i,j] = num_iters

def in_mandelbrot(c,iters):
    in_set = True
    z = 0
    i = 0
    while in_set and i < iters:
        z = z**2 + c
        if np.absolute(z) > 2:
            in_set = False
        i+=1
    return in_set, i

def colour(params,state):
    match params.render_mode:
        case "grayscale":
            state.img = Image.fromarray(np.uint8(255*(state.result/params.max_iter)))
        case "hue":
            hsv = np.uint8(255*
                np.stack((
                    state.result/params.max_iter,
                    np.ones((h,w)),
                    np.ones((h,w))
                ),axis=-1)
            )
            state.img = Image.fromarray(hsv,mode='HSV')
            state.img = state.img.convert('RGB')