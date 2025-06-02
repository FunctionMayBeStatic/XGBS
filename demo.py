import scipy
import xgbs

hsi = scipy.io.loadmat('Indian_pines.mat')['indian_pines']
gt = scipy.io.loadmat('Indian_pines_gt.mat')['indian_pines_gt']

selected_bands = xgbs.band_selection(
    hsi_3d=hsi,
    gt_2d=gt,
    nbs=5,
    alpha=0.6,
    beta=2.0
)
print(selected_bands)
