# 🌳 XGBS
> classification task-driven hyperspectral band selection via interpretability from XGBoost

The source code and pip version of XGBS will be made public following the publication of the paper:
"Classification Task-Driven Hyperspectral Band Selection via Interpretability from XGBoost"

**How to use:**

1 Install XGBS
   
```
pip install xgbs 
```
2 Run:
```
import xgbs
import scipy
hsi_3d = scipy.io.loadmat("/path/to/your/dataset/Indian_pines.mat')["indian_pines"]
gt_2d = scipy.io.loadmat("/path/to/your/dataset/Indian_pines_gt.mat')["indian_pines_gt"]
hsi_2d = hsi_3d[gt_2d != 0]
gt_1d = gt_2d[gt_2d != 0]

selected_bands = xgbs.select_bands(hsi_2d, gt_1d, num_band=5)
print(selected_bands)
```
