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
        default=False,
        help="Print params after loading",
    )
    parser.add_argument(
        "--fractal",
        type=str,
        default="mandelbrot", # or others TBA
        help="Fractal type",
    )
    parser.add_argument(
        "--matrix",
        type=str,
        default="",
        help="String representation of matrix for bohemian",
    )
    parser.add_argument(
        "--distribution",
        type=str,
        default="",
        help="String representation of distribution for bohemian",
    )
    parser.add_argument(
        "--render_mode",
        type=str,
        default="grayscale",
        help="Render mode"
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
    parser.add_argument(
        "--max_iter",
        type=float,
        default=100,
        help="Max iters",
    )

    return parser

def load_params_from_json(params: Namespace) -> None:
    with open(params.param_file, "r") as f:
        f_text = f.read()
    dic = json.loads(f_text)
    for k,v in dic.items():
        setattr(params,k,v)

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
    
    h = int((bounds['ymax'] - bounds['ymin'])/params.resolution)
    w = int((bounds['xmax'] - bounds['xmin'])/params.resolution)

    return h, w

def string_to_list(str):
    # Remove the square brackets and split into rows
    rows = str[1:-1].split("],[")
    matrix = []
    num_placeholders = 0
    # Split each row into its individual elements and create the new matrix
    for row in rows:
        elements = row.split(",")
        for ind, ele in enumerate(elements):
            if ele.isnumeric():
                elements[ind] = int(ele)
            else: # it's a placeholder for a random variable
                num_placeholders += 1
        matrix.append(elements)
    return matrix, num_placeholders