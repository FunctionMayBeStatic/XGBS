# 🌳 XGBS
> An advanced supervised hyperspectral band selection method

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](https://doi.org/10.1109/JSTARS.2025.3572278) [![PyPI Version](https://img.shields.io/pypi/v/your-package-name.svg)](https://pypi.org/project/your-package-name/)


# Article
[Classification Task-Driven Hyperspectral Band Selection via Interpretability from XGBoost](https://ieeexplore.ieee.org/document/11008687)
💡 note: This is an open-access journal.
*Abstract*
> Band selection (BS) identifies key bands from hyperspectral imagery (HSI) for specific downstream tasks, playing a pivotal role in practical applications. eXtreme Gradient Boosting (XGBoost), an interpretable tree-based ensemble learning classifier, explicitly implements the complex nonlinear hyperspectral classification. The interpretable information extracted from tree structure offers a novel basis for supervised BS. To this end, this paper proposes a supervised BS method, named classification task-driven hyperspectral band selection via interpretability from XGBoost (XGBS). It leverages prior knowledge to train a classification task-driven XGBoost, and interprets tree structure to extract multivariate interpretable information, encompassing band split gain and two types of band dependencies. Subsequently, a heuristic search framework is employed to evaluate band performance, facilitating the selection of bands with strong classification capability, high interdependency and low redundancy. Experiments conducted on six real HSI datasets demonstrate the effectiveness and stability of the proposed XGBS.

*Overall structure of XGBS*
