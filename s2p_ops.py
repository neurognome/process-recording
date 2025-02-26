default_ops = {
    # general
    'diameter': 10,
    'fast_disk': '/mnt/fast',
    'do_bidiphase': False,
    'save_mat': False,
    'save_NWB': False,
    'tau': 1.3,
    'combined': False,
    
    # registration
    'do_registration': True, # force re-registration
    'keep_movie_raw': True, # must be true for 2 step reg
    'two_step_registration': True,
    'nimg_init': 800, # subsampled frames for finding reference image
    'batch_size': 2000, #2000, # number of frames per batch, default=500
    'align_by_chan': 1, # 1-based, use 2 for tdT
    'reg_tif': True,
    'reg_tif_chan2': True,
    
    # non rigid registration settings
    'nonrigid': True, # whether to use nonrigid registration
    
    # cell extraction
    'denoise': False,
    'threshold_scaling': 1, # adjust the automatically determined threshold by this scalar multiplier, was 1. (WH) # 0.6 for low signal, default 5
    'sparse_mode': False,
    'max_iterations': 50, # usualy stops at threshold scaling, default 20
    'high_pass': 100,  # running mean subtraction with window of size 'high_pass' (use low values for 1P), default 100
    # 'classifier_path': 'c:/users/will/code/suite2p/suite2p/classifiers/classifier_8m.npy',
    
    # deconvolution settings
    'baseline': 'maximin',  # baselining mode (can also choose 'prctile')
    'win_baseline': 60.,  # window for maximin
    'sig_baseline': 10.,  # smoothing constant for gaussian filter
    'prctile_baseline': 8.,  # optional (whether to use a percentile baseline)
    'neucoeff': 0.7,  # neuropil coefficient
    
    # custom settings
    'remove_artifacts': (75, 512-75)
}

register_only = {
    'reg_tif': True,
    'roidetect': False,
    'fast_disk': '/mnt/fast',
}

# these settings are taken from run_s2p_8m.py
gcamp8m  = {
    # general
    'diameter': 8,
    'fast_disk': '/mnt/fast',
    'do_bidiphase': True,
    'save_mat': False,
    'save_NWB': False,
    'tau': 0.05,
    # 'preclassify': 0., # apply classifier before signal extraction with a prob of 0.3
    'combined': False,
    
    # registration
    'do_registration': True, # force re-registration
    'keep_movie_raw': False, # must be true for 2 step reg
    'two_step_registration': False,
    'nimg_init': 800, # subsampled frames for finding reference image
    'batch_size': 2000, #2000, # number of frames per batch, default=500
    'align_by_chan': 1, # 1-based, use 2 for tdT
    
    # non rigid registration settings
    'nonrigid': False, # whether to use nonrigid registration
    
    # cell extraction
    'denoise': False,
    'threshold_scaling': 0.6, # adjust the automatically determined threshold by this scalar multiplier, was 1. (WH) # 0.6 for low signal, default 5
    'sparse_mode': False,
    'max_iterations': 50, # usualy stops at threshold scaling, default 20
    'high_pass': 100,  # running mean subtraction with window of size 'high_pass' (use low values for 1P), default 100
    # 'classifier_path': 'c:/users/will/code/suite2p/suite2p/classifiers/classifier_8m.npy',
    
    # deconvolution settings
    'baseline': 'maximin',  # baselining mode (can also choose 'prctile')
    'win_baseline': 60.,  # window for maximin
    'sig_baseline': 10.,  # smoothing constant for gaussian filter
    'prctile_baseline': 8.,  # optional (whether to use a percentile baseline)
    'neucoeff': 0.7,  # neuropil coefficient

    # classifier settings
    'classifier_path': '/home/kevinsit/.suite2p/classifiers/gcamp8m.npy',
    # 'preclassify': 0., # apply classifier before signal extraction with a prob of 0.3

    # custom settings
    # 'remove_artifacts': (100, 512-100)
}

red  = {
    # general
    # 'diameter': 8,
    'fast_disk': '/mnt/fast',
    'do_bidiphase': True,
    'save_mat': False,
    'save_NWB': False,
    'tau': 1,
    'combined': False,

    # cellpose
    'anatomical_only': 1,

    # registration
    'do_registration': True, # force re-registration
    'keep_movie_raw': False, # must be true for 2 step reg
    'two_step_registration': False,
    'nimg_init': 800, # subsampled frames for finding reference image
    'batch_size': 2000, #2000, # number of frames per batch, default=500
    'align_by_chan': 2, # 1-based, use 2 for tdT
    
    # non rigid registration settings
    'nonrigid': False, # whether to use nonrigid registration
    
    # cell extraction
    'denoise': False,
    'threshold_scaling': 0.6, # adjust the automatically determined threshold by this scalar multiplier, was 1. (WH) # 0.6 for low signal, default 5
    'sparse_mode': False,
    'max_iterations': 50, # usualy stops at threshold scaling, default 20
    'high_pass': 100,  # running mean subtraction with window of size 'high_pass' (use low values for 1P), default 100
    
    'spikedetect': False, 
    # custom settings
    # 'remove_artifacts': (100, 512-100)
}
