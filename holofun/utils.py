from pathlib import Path
import platform
import time
import functools
import os
import logging
from collections import defaultdict

def make_results_folder(root, mouse, date, folder_name='results', chdir=True):
    """
    Creates a folder named 'results' for the mouse at root/mouse/date/results. Optionally changes 
    the working directory to the results folder. Can specify a folder name other than results or
    set as empty string.

    Args:
        root (str): root path or folder to save into
        mouse (str): name of mouse
        date (str): date of experiment
        folder_name (str): name of folder to save to. leave empty to save to 
                           root/mouse/name. Defaults to 'results'.
        chdir (bool, optional): whether to change the cwd to results folder. Defaults to True.

    Returns:
        pathlib.Path: path to results folder
    """
    results = Path(root, mouse, date, folder_name)
    results.mkdir(exist_ok=True, parents=True)
    if chdir:
        os.chdir(results)
        print(f'Set cwd to: {os.getcwd()}')
    return results

def tic():
    """Records the time in highest resolution possible for timing code."""
    return time.perf_counter()

def toc(tic):
    """Returns the time since 'tic' was called."""
    return time.perf_counter() - tic

def ptoc(tic, start_string='Time elapsed:', end_string='s'):
    """
    Print a default or custom print statement with elapsed time. Both the start_string
    and end_string can be customized. Autoformats with single space between start, time, 
    stop. Returns the time elapsed.

    Format -> 'start_string' + 'elapsed time in seconds' + 'end_string'.
    Default -> start_string = 'Time elapsed:', end_string = 's'.
    """
    t = toc(tic)
    pstring = ' '.join([start_string, f'{t:.4f}', end_string])
    print(pstring)
    return t

def ptoc_min(tic, start_string='Time elapsed:', end_string='min'):
    """See ptoc. Modified for long running processes."""
    t = toc(tic)
    pstring = ' '.join([start_string, f'{t/60:.2f}', end_string])
    print(pstring)
    return t

def tictoc(func):
    """Prints the runtime of the decorated function."""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f'<{func.__module__}.{func.__name__}> done in {run_time:.3f}s')
        return value
    return wrapper_timer

def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")
        return value
    return wrapper_debug

def verifyrun(func):
    """Prints whether the decorated function ran."""
    @functools.wraps(func)
    def wrapper_verifyrun(*args, **kwargs):
        print(f'Ran {func.__name__!r} from {func.__module__}.')
        value = func(*args, **kwargs)
        return value
    return wrapper_verifyrun

def replace_tup_ix(tup, ix, val):
    return tup[:ix] + (val,) + tup[ix+1:]

def nbsetup():
    try:
        if __IPYTHON__:
            get_ipython().magic('load_ext autoreload')
            get_ipython().magic('autoreload 3')
            get_ipython().magic('matplotlib inline')
            get_ipython().magic("config InlineBackend.figure_format = 'retina'")
    except NameError:
        pass
    
    try:
        import seaborn as sns
        sns.set_style('ticks',{'axes.spines.right': False, 'axes.spines.top': False}) # removes annoying top and right axis
        sns.set_context('notebook') # can change to paper, poster, talk, notebook
    except ModuleNotFoundError:
        logging.warning('Failed to import seaborn.')
        
    try:
        import pandas as pd
        pd.set_option('display.max_columns',10) # limits printing of dataframes
    except ModuleNotFoundError:
        logging.warning('Failed to import pandas.')

    try:
        import matplotlib as mpl
        # mpl.rcParams['savefig.dpi'] = 600 # default resolution for saving images in matplotlib
        mpl.rcParams['savefig.format'] = 'pdf' # defaults to png for saved images (SVG is best, however)
        mpl.rcParams['savefig.bbox'] = 'tight' # so saved graphics don't get chopped
        mpl.rcParams['image.cmap'] = 'viridis'
        mpl.rcParams['ps.fonttype'] = 42
        mpl.rcParams['savefig.transparent'] = True
        mpl.rcParams['pdf.fonttype'] = 42
        # add to remove seaborn dependency
        mpl.rcParams['axes.spines.top'] = False
        mpl.rcParams['axes.spines.right'] = False
        # mpl.rcParams['font.size'] = 10
        mpl.rcParams['figure.constrained_layout.use'] = True
    except ModuleNotFoundError:
        logging.warning('Failed to import matplotlib.')

def flatten(t):
    return [item for sublist in t for item in sublist]

def make_paths(mouse, date, result_base, tiff_base='f:/experiments', 
               franken_drive='x', must_exist=True, keys=('srv', 'e', 'tiffs')):
    
    tiff_base = tiff_base.replace(':','').split('/')
    
    if platform.system() == 'Linux':
        franken = Path('/mnt/franken')
        edrive = Path('/mnt/e/', result_base, mouse, date)
        tiff_path = Path('/mnt', *tiff_base, mouse, date)
        
    else:
        franken = Path(franken_drive + ':/')
        edrive = Path('e:/', result_base, mouse, date)
        tiff_path = Path(tiff_base[0]+':/',tiff_base[1], mouse, date)
    
    drives = (franken, edrive, tiff_path)
    
    # only check hdd locations as optional files might not exist
    if must_exist:
        doesnt_exist = [not drive.exists() for drive in drives]
        
        if any(doesnt_exist):
            non_existing = [drive for drive,exist in zip(drives,doesnt_exist) if exist]
            raise FileNotFoundError(f'Could not find one or more of the paths. {non_existing}')
    
    paths = dict(zip(keys, drives))
    
    # find etc specific files
    # globbed items can be handled the same way 
    handle_globs = {
        'setupdaq': tiff_path.glob(date[2:]+'*.mat'),
        's2p': edrive.rglob('suite2p'),
        'clicked_cells': tiff_path.glob('*clicked*.npy'),
        'mm3d': tiff_path.rglob('makeMasks3D_img.mat'),
        'img920': tiff_path.rglob('*920_*.tif*'),
        'img1020': tiff_path.rglob('*1020_*.tif*'),
        'img800': tiff_path.rglob('*800_*.tif*'),
        'ori': tiff_path.rglob('*ori*.mat'),
        'ret': tiff_path.rglob('*ret*.mat'),
        'si_online': tiff_path.rglob('*IntegrationRois*.csv')
    }
    
    # assign vals in path dict
    for k,v in handle_globs.items():
        v = list(v)
        if len(v) == 1:
            paths[k] = v[0]
        elif len(v) > 1:
            paths[k] = v
        else:
            paths[k] = 'path NA'
        
    return paths   

def cm_to_inch(value):
    return value/2.54