# 🌳 XGBS
> An advanced supervised hyperspectral band selection method

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](https://doi.org/10.1109/JSTARS.2025.3572278) [![PyPI Version](https://img.shields.io/pypi/v/your-package-name.svg)](https://pypi.org/project/your-package-name/)




The source code and pip version of XGBS will be made public following the publication of the paper:
"Classification Task-Driven Hyperspectral Band Selection via Interpretability from XGBoost"


**How to use:**

1 Install XGBS
   
```
pip install xgbs 
```
2 Run
```
import xgbs
import scipy

hsi_3d = scipy.io.loadmat("/path/to/your/dataset/Indian_pines.mat")["indian_pines"]
gt_2d = scipy.io.loadmat("/path/to/your/dataset/Indian_pines_gt.mat")["indian_pines_gt"]
hsi_2d = hsi_3d[gt_2d != 0]
gt_1d = gt_2d[gt_2d != 0]

selected_bands = xgbs.select_bands(hsi_2d, gt_1d, num_band=5)
print(selected_bands)
```
