from nilearn.image import load_img
from fMRIpreprocessing import utils
import numpy as np
import random

image_path = "data/raw/1.nii.gz"
regs_path = "data/raw/1.txt"
num_rois = 100
image = load_img(image_path)
fmri = image.get_fdata()
# reproducability
seed = 789
random.seed(seed)
np.random.seed(seed)

parcels = utils.parcellation(fmri, num_rois)
Y = utils.remove_drifts(parcels)
regs = np.loadtxt(regs_path)
Y = utils.regress_head_motions(Y, regs)
corr = utils.construct_corr(Y)

print("The data has been successfully preprocessed!",corr.shape)
