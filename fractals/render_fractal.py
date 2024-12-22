import sys
import os
#from numpy import ndarray
from fractals import *
import importlib
import json

def main() -> None:

    state = State()
       
    # parse arguments from params.json into variable params
    # TODO get rid of argparse and just load from json
    parser = read_params()
    params, _ = parser.parse_known_args()
    load_params_from_json(params)

    # setup fractal height and width
    height, width = get_height_width(params)
    setattr(params,'height',height)
    setattr(params,'width',width)
    
    # run module for the fractal we want to render
    mod = importlib.import_module("fractals."+params.fractal)
    mod.render(params,state)

    state.img.save('image.png')

    if params.print_params:
        print_params(params=params)


if __name__ == "__main__":
    main()



