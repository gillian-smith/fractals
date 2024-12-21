import sys
import os
#from numpy import ndarray
from fractals import *
import importlib

def main() -> None:

    state = State()
       
    # parse arguments from params.json into variable params
    parser = read_params()
    params, _ = parser.parse_known_args()

    # setup fractal height and width
    height, width = get_height_width(params)
    setattr(params,'height',height)
    setattr(params,'width',width)
    
    # run module for the fractal we want to render
    mod = importlib.import_module("fractals."+params.fractal)
    mod.render(params,state)

    if params.print_params:
        print_params(params=params)


if __name__ == "__main__":
    main()



