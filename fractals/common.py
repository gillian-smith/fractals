import os, json
import argparse
from argparse import ArgumentParser, Namespace
import importlib

class State:
    pass

def read_params() -> argparse.ArgumentParser:
    parser = ArgumentParser(
        description="read params from file"
    )
    parser.add_argument(
        "--param_file",
        type=str,
        default="params.json",
        help="Filepath for the JSON parameter file",
    )
    parser.add_argument(
        "--print_params",
        action="store_false",
        default=True,
        help="Print params after loading",
    )
    parser.add_argument(
        "--fractal",
        type=str,
        default="mandelbrot", # or others TBA
        help="Fractal type",
    )
    parser.add_argument(
        "--bounds",
        type=list,
        default=[-2,-2,2,2],
        help="Display bounds: xmin, ymin, xmax, ymax",
    )
    parser.add_argument(
        "--resolution",
        type=float,
        default=0.005,
        help="Pixel width",
    )

    return parser

# Print parameters in screen and a dedicated file
def print_params(params: Namespace) -> None:
    param_file = params.param_file[:-5]
    param_file = param_file + "_saved.json"

    # load the given parameters
    with open(param_file, "w") as json_file:
        json.dump(params.__dict__, json_file, indent=2)

    os.system("echo rm " + param_file + " >> clean.sh")



# helper functions

def get_bounds(params):
    b = dict()
    for index, key in enumerate(['xmin','ymin','xmax','ymax']):
        b[key] = params.bounds[index]
    return b

def get_height_width(params):
    bounds = get_bounds(params)

    assert bounds['ymax'] > bounds['ymin'], "Ensure ymin < ymax"
    assert bounds['xmax'] > bounds['xmin'], "Ensure xmin < xmax"
    
    h = (bounds['ymax'] - bounds['ymin'])/params.resolution
    w = (bounds['xmax'] - bounds['xmin'])/params.resolution

    return h, w