import re
import copy
import numpy as np


def normalize(x):
    val_max, val_min = np.max(x), np.min(x)
    if (val_max - val_min) == 0:
        return 0
    return (x - val_min) / (val_max - val_min)


class CARTTree:
    MAX_DEPTH = 10

    def __init__(self, str_tree):
        self.str_tree = str_tree
        self.node_list = []

        # parse nodes.
        for line in str_tree.split('\n'):
            if node_info := self._re_match_node(line):
                self.node_list.append(node_info)

        if len(self.node_list) == 0:
            return

        # get level weights and weight nodes.
        level_covers = np.zeros((self.MAX_DEPTH,))
        for node in self.node_list:
            level_covers[node['level']] += node['cover']

        self.level_weights = level_covers / np.sum(level_covers)
        for node in self.node_list:
            w = self.level_weights[node['level']]
            node['level_weighted_cover'] = float(node['cover'] * w)

        # find all prediction path.
        self.all_path = []
        self._find_all_path_recursion(0, [])
        for node in self.node_list:
            band = node['band']
            for path in self.all_path:
                if band in path:
                    node['same_path'] += copy.deepcopy(path)
            node['same_path'] = list(set(node['same_path']))

        # find same level.
        for target_node in self.node_list:
            for node in self.node_list:
                if target_node['level'] == node['level']:
                    target_node['same_level'].append(node['band'])
            target_node['same_level'] = list(set(target_node['same_level']))

    def _find_all_path_recursion(self, idx, path):
        path = copy.deepcopy(path)
        target_node = None
        for node in self.node_list:
            if node['idx'] == idx:
                target_node = node
                break
        if target_node is None:
            self.all_path.append(path)
        else:
            path.append(target_node['band'])
            self._find_all_path_recursion(target_node['y'], path)
            self._find_all_path_recursion(target_node['n'], path)

    def get_same_path_relations(self, band_exist):
        for node in self.node_list:
            if band_exist in node['same_path']:
                yield node['band'], node['level_weighted_cover']

    def get_same_level_relations(self, band_exist):
        for node in self.node_list:
            if band_exist in node['same_level']:
                yield node['band'], node['level_weighted_cover']

    @classmethod
    def _re_match_node(cls, line):
        if len(line) == 0 or line.find('leaf=') != -1:
            return None
        else:
            pattern = r'\t*(\d+):\[f(\d+)\<.*yes=(\d+),no=(\d+),.*cover=(\d+\.?\d*)'
            match_res = re.match(pattern, line)
            return {
                'idx': int(match_res.group(1)),
                'level': len(line) - len(line.lstrip('\t')),
                'band': int(match_res.group(2)),
                'y': int(match_res.group(3)),
                'n': int(match_res.group(4)),
                'cover': float(match_res.group(5)),
                'level_weighted_cover': None,
                'same_path': [],
                'same_level': [],
            }


def parse_trees(str_tree_list, num_band):
    dep_level = np.zeros((num_band, num_band))
    dep_path = np.zeros((num_band, num_band))
    for str_tree in str_tree_list:
        ct = CARTTree(str_tree)
        for band_exist in range(num_band):
            pass
            for band_target, cover in ct.get_same_level_relations(band_exist):
                dep_level[band_exist, band_target] += cover
            for band_target, cover in ct.get_same_path_relations(band_exist):
                dep_path[band_exist, band_target] += cover
    for b in range(num_band):
        dep_level[b, b] = 0
        dep_path[b, b] = 0
    return dep_level, dep_path


def get_all_bands_redundancy(hsi_3d, gt_2d):
    num_band = hsi_3d.shape[2]
    hsi_3d = normalize(hsi_3d)
    hsi_2d = hsi_3d[gt_2d != 0]
    all_bands_redundancy = np.zeros((num_band, num_band), dtype=np.float32)
    for i in range(num_band - 1):
        for j in range(i, num_band):
            band_im_i = hsi_2d[:, i]
            band_im_j = hsi_2d[:, j]
            if np.std(band_im_i) == 0:  # prevent std == 0 and corr == Nan.
                band_im_i[0] += 0.001
            if np.std(band_im_j) == 0:
                band_im_j[0] += 0.001
            corr = np.abs(np.corrcoef(band_im_i, band_im_j)[0, 1])
            all_bands_redundancy[i, j] = corr
            all_bands_redundancy[j, i] = corr
    return all_bands_redundancy


def gauss_weighting(mat, det=150, clip=0.9):
    num_band = mat.shape[0]
    mat = np.clip(mat, a_min=0.9, a_max=1)
    mask = np.zeros((num_band, num_band))
    for i in range(num_band):
        for j in range(i, num_band):
            val = np.exp(- (i - j) ** 2 / (2 * det ** 2))
            mask[i, j] = val
            mask[j, i] = val
    mask = normalize(mask)
    mat_weighted = np.multiply(mat, mask)
    return mat_weighted
