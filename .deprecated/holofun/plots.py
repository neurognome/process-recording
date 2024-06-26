import numpy as np
import matplotlib.pyplot as plt

from .stats import sem

def scatter2hist(x, y, bins=(10,10), ax=None, do_log=False, **kwargs):
    """Generate a 2D histogram from scatter plot data. Bins can be int or tuple."""
    if ax is None:
        ax = plt.gca()
    h, *_ = np.histogram2d(x, y, bins=bins)
    if do_log:
        h = np.log(h)
    ax.imshow(np.rot90(h), interpolation='nearest', **kwargs)
    return ax
    
def plot_mean_dff(trwise_data, cells=None, trials=None, xvals=None, ax=None, **kwargs):
    if ax is None:
       fig, ax = plt.subplots(1,1, figsize=(4,4), constrained_layout=True)
       
    if cells is None:
        cells = np.arange(trwise_data.shape[1])
    if trials is None:
        trials = np.arange(trwise_data.shape[0])
    
    mask = np.ix_(trials, cells)
    
    mm = trwise_data[mask].mean(0).mean(0)
    err = sem(trwise_data[mask].mean(0), 0)
    
    if xvals is None:
        x = np.arange(mm.size)
    else:
        x = xvals
    
    ax.plot(x, mm, **kwargs)
    ax.fill_between(x, mm+err, mm-err, alpha=0.5, **kwargs)
    
    return ax

def plot_mean_dff_by_cell(trwise_data, cells=None, trials=None, xvals=None, ax=None, **kwargs):
    if ax is None:
       fig, ax = plt.subplots(1,1, figsize=(4,4), constrained_layout=True)
       
    if cells is None:
        cells = np.arange(trwise_data.shape[1])
    if trials is None:
        trials = np.arange(trwise_data.shape[0])
    
    mask = np.ix_(trials, cells)
    
    mm = trwise_data[mask].mean(0)
    err = sem(trwise_data[mask], 0)
    
    if xvals is None:
        x = np.arange(mm.shape[-1])
    else:
        x = xvals
    
    for c,m,e in zip(cells, mm, err):
        ax.plot(x, m, label=c, **kwargs)
        ax.fill_between(x, m+e, m-e, alpha=0.5, **kwargs)

    return ax

def plot_mean_dff_of_cell(trwise_data, cell, trials=None, xvals=None, ax=None, **kwargs):
    if ax is None:
       fig, ax = plt.subplots(1,1, figsize=(4,4), constrained_layout=True)
       
    if trials is None:
        trials = np.arange(trwise_data.shape[0])
    
    mask = np.ix_(trials, [cell])
    
    mm = trwise_data[mask].mean(0).squeeze()
    err = sem(trwise_data[mask], 0).squeeze()
    
    if xvals is None:
        x = np.arange(mm.size)
    else:
        x = xvals
    
    ax.plot(x, mm, label=cell, **kwargs)
    ax.fill_between(x, mm+err, mm-err, alpha=0.5, **kwargs)

    return ax

def plot_tc(d, cell, drop_grey_screen=True, ax=None, **kwargs):
    """Give a mean DataFrame and a cell number, plot the tuning curve."""
    if ax is None:
        fig, ax = plt.subplots(1,1, figsize=(3,3), constrained_layout=True)
        
    if drop_grey_screen:
        vals = d.loc[d.ori >= 0].copy()
        
    m = vals[vals.cell == cell].groupby('ori').mean()['df']
    e = vals[vals.cell == cell].groupby('ori').sem()['df']
    xs = vals.ori.unique()
    
    kwargs.setdefault('linewidth', 2)
    
    ax.errorbar(xs, m, e, **kwargs)
    ax.set_ylabel('$\Delta$F/F')
    ax.set_xticks(xs)
    ax.set_xticklabels(xs, rotation=-45)
    
    return ax

def plot_cell_ret(ret_data, ret_fit):
    fig, ax = plt.subplots(1,3, figsize=(10,10))

    x,y,_ = ret_fit.calculate_grid()
    ext = (x.min(), x.max(), y.min(), y.max())
    ax[0].imshow(ret_data, extent=ext)
    ax[0].set_title('Data')
    ret_fit.plot(ax=ax[1])
    ax[1].set_title('Fit')
    ax[2].set_title('Model')
    ret_fit.plot(expand_by=100, ax=ax[2])

    for a in ax:
        a.axis('off')
        
    fig.subplots_adjust(wspace=.01, hspace=.01)
    plt.show()
    
def update_all(axes, **kwargs):
    for ax in axes.ravel():
        for k,v in kwargs.items():
            fxn = eval(f'ax.{k}')
            fxn(v)