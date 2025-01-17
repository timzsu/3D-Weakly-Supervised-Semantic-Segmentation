'''
config.py
Written by Li Jiang
Modified by Su Zhengyuan
'''

import argparse
import yaml
import os
from easydict import EasyDict as edict

def get_parser():
    parser = argparse.ArgumentParser(description='Point Cloud Segmentation')
    parser.add_argument('--config', type=str, default='config/3DUNetWithText_scannet_default.yaml', help='path to config file')

    ### pretrain
    parser.add_argument('--pretrain', type=str, default='', help='path to pretrain model')

    args_cfg = parser.parse_args()
    assert args_cfg.config is not None
    with open(args_cfg.config, 'r') as f:
        config = yaml.safe_load(f)
    for key in config:
        for k, v in config[key].items():
            if isinstance(v, dict):
                v = edict(v)
            setattr(args_cfg, k, v)

    return args_cfg

cfg = get_parser()
setattr(cfg, 'exp_path', os.path.join('exp', cfg.training_name, cfg.training_name))
