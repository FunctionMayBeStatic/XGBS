import numpy as np
from xgboost import XGBClassifier
from .tools import normalize, parse_trees, get_all_bands_redundancy, gauss_weighting


def band_selection(hsi_3d, gt_2d, nbs, alpha=0.1, beta=0.1):
    """ select bands. """

    # 1. prepare data.
    num_band = hsi_3d.shape[2]
    hsi_3d = normalize(hsi_3d)
    h2d = hsi_3d[gt_2d != 0]
    g1d = gt_2d[gt_2d != 0]

    # 2. train XGBoost.
    xgb_model = XGBClassifier(
        n_estimators=128,  # ------------------ num trees.
        max_depth=10,  # ---------------------- max tree depth.
        objective='binary:logistic',  # ------- binary cross-entropy loss.
        booster='gbtree',  # ------------------ gradient boosting.
        gamma=0,  # --------------------------- min gain to split.
        min_child_weight=1,  # ---------------- min num of sample in node.
        subsample=1,  # ----------------------- no random.
        colsample_bytree=1,  # ---------------- no random.
        reg_alpha=0,  # ----------------------- L1 constrain to leaf values.
        reg_lambda=1,  # ---------------------- L2 constrain to leaf values.
        seed=0,
        importance_type='gain'
    )
    xgb_model.fit(h2d, g1d - 1)
    # pred = xgb_model.predict(h2d)
    # oa = float(np.average(pred == g1d - 1))

    # 3. extract MII.
    vec_q = xgb_model.feature_importances_  # importance_type:gain
    booster = xgb_model.get_booster()
    str_tree_list = booster.get_dump(with_stats=True)
    mat_dl, mat_dp = parse_trees(str_tree_list, num_band)
    mat_r = get_all_bands_redundancy(hsi_3d, gt_2d)

    # 4. heuristic search.
    mat_d = mat_dl + beta * mat_dp
    mat_r = gauss_weighting(mat_r, det=20)
    first_band = int(np.argmax(vec_q))
    selected_bands = [first_band]
    for idx_search in range(nbs - 1):
        vec_q = normalize(vec_q)
        vec_d = normalize(np.average(mat_d[selected_bands], axis=0))
        ref = normalize(np.max(mat_r[selected_bands, :], axis=0))
        score1 = normalize(vec_q * (1 - ref))
        score2 = score1 + alpha * vec_d
        score2[selected_bands] = 0
        next_band = np.argmax(score2)
        selected_bands.append(int(next_band))
    return selected_bands
