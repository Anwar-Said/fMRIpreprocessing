from nilearn.datasets import fetch_atlas_schaefer_2018
from nilearn.image import load_img
from nilearn.connectome import ConnectivityMeasure
from scipy.stats import zscore
# from scipy import zscore_sample
import numpy as np


def parcellation(fmri, n_rois=100):
    """
    Prepfrom brain parcellation

    Args:

    fmri (numpy array): fmri image
    rois (int): {100, 200, 300, 400, 500, 600, 700, 800, 900, 1000}, optional,
    Number of regions of interest. Default=1000.
    
    """
    roi = fetch_atlas_schaefer_2018(n_rois=n_rois,
                                    yeo_networks=17,
                                    resolution_mm=2)
    atlas = load_img(roi['maps'])
    volume = atlas.get_fdata()
    subcor_ts = []
    for i in np.unique(volume):
        if i != 0:
            bool_roi = np.zeros(volume.shape, dtype=int)
            bool_roi[volume == i] = 1
            bool_roi = bool_roi.astype(bool)
            roi_ts_mean = []
            for t in range(fmri.shape[-1]):
                roi_ts_mean.append(np.mean(fmri[:, :, :, t][bool_roi]))
            subcor_ts.append(np.array(roi_ts_mean))

    Y = np.array(subcor_ts).T
    return Y


def remove_drifts(Y):
    """
    This function removes the scanner drifts in the fMRI signals that arise from instrumental factors. By eliminating these trends, we enhance the signal-to-noise ratio and increase the sensitivity to neural activity.
    
    """
    start = 1
    stop = Y.shape[0]
    step = 1
    t = np.arange(start, stop + step, step)
    tzd = zscore(np.vstack((t, t**2)), axis=1)
    XX = np.vstack((np.ones(Y.shape[0]), tzd))
    B = np.matmul(np.linalg.pinv(XX).T, Y)
    Yt = Y - np.matmul(XX.T, B)
    return Yt


def regress_head_motions(Y, regs):
    """
    This function regress out six rigid- body head motion parameters, along with their derivatives, from the fMRI data
    
    Args:
    Y (numpy array)): fmri image
    regs (numpy array): movement regressor
    """
    B2 = np.matmul(np.linalg.pinv(regs), Y)
    m = Y - np.matmul(regs, B2)
    return m

def construct_corr(m):
    """
    This function construct correlation matrix from the preprocessed fmri matrix
    Args.

    m (numpy  array): a preprocessed numpy matrix
    return: correlation matrix
    """
    zd_Ytm = (m - np.nanmean(m, axis=0)) / np.nanstd(m, axis=0, ddof=1)
    conn = ConnectivityMeasure(kind='correlation')
    fc = conn.fit_transform([m])[0]
    zd_fc = conn.fit_transform([zd_Ytm])[0]
    fc *= np.tri(*fc.shape)
    np.fill_diagonal(fc, 0)
    # zscored upper triangle
    zd_fc *= 1 - np.tri(*zd_fc.shape, k=-1)
    np.fill_diagonal(zd_fc, 0)
    corr = fc + zd_fc
    return corr
