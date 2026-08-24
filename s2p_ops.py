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
    'reg_tif': False,
    'reg_tif_chan2': False,
    
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
    # 'auto' -> bounds detected per-recording by helpers.artifacts.detect_artifact_bounds,
    # then floored at s2p_cli.ARTIFACT_MIN_CROP px/side (currently 150) to cover the
    # contaminated penumbra past the visible band.
    # (set a fixed tuple e.g. (100, 512-100) to override with a manual crop, which
    #  bypasses both detection and the floor)
    'remove_artifacts': 'auto'}

voltage = {
    # general
    'diameter': 10,
    'fast_disk': '/mnt/fast',
    'do_bidiphase': False,
    'save_mat': False,
    'save_NWB': False,
    'tau': 0.5,
    'combined': False,
    
    # registration
    'do_registration': True, # force re-registration
    'keep_movie_raw': True, # must be true for 2 step reg
    'two_step_registration': True,
    'nimg_init': 800, # subsampled frames for finding reference image
    'batch_size': 2000, #2000, # number of frames per batch, default=500
    'align_by_chan': 1, # 1-based, use 2 for tdT
    'reg_tif': False,
    
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

    # Explicitly no crop. Set to 'auto' if this preset is ever run on the
    # holography rig -- but note the floor in s2p_cli is enforced even when no
    # band is detected, so 'auto' ALWAYS removes ARTIFACT_MIN_CROP px/side
    # (currently 150 of a 512 frame per side). Do not enable it blindly.
    'remove_artifacts': None,
}

spines = {
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
    'align_by_chan': 2, # 1-based, use 2 for tdT
    'reg_tif': False,
    'reg_tif_chan2': False,
    
    # non rigid registration settings
    'nonrigid': True, # whether to use nonrigid registration
    
    # cell extraction
    'denoise': True,
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

    # Explicitly no crop. Set to 'auto' if this preset is ever run on the
    # holography rig -- but note the floor in s2p_cli is enforced even when no
    # band is detected, so 'auto' ALWAYS removes ARTIFACT_MIN_CROP px/side
    # (currently 150 of a 512 frame per side). Do not enable it blindly.
    'remove_artifacts': None,
}

register_only = {
    'reg_tif': True,
    'reg_tif_chan2': True,
    'roidetect': False,
    'fast_disk': '/mnt/fast',

    # Explicitly no crop. Set to 'auto' if this preset is ever run on the
    # holography rig -- but note the floor in s2p_cli is enforced even when no
    # band is detected, so 'auto' ALWAYS removes ARTIFACT_MIN_CROP px/side
    # (currently 150 of a 512 frame per side). Do not enable it blindly.
    'remove_artifacts': None,
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
    # holography rig -> detect and crop the photostim edge bands. 'auto' is
    # resolved in s2p_cli by detect_artifact_bounds, then floored at
    # ARTIFACT_MIN_CROP px/side. Needs the lab suite2p fork (neurognome/suite2p);
    # upstream MouseLand ignores the key and silently gives you uncropped data.
    'remove_artifacts': 'auto',
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
    # holography rig -> detect and crop the photostim edge bands. 'auto' is
    # resolved in s2p_cli by detect_artifact_bounds, then floored at
    # ARTIFACT_MIN_CROP px/side. Needs the lab suite2p fork (neurognome/suite2p);
    # upstream MouseLand ignores the key and silently gives you uncropped data.
    'remove_artifacts': 'auto',
}
