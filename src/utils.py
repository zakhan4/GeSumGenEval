import os
from os.path import exists, join
import json

def read_jsonl(path):
    data = []
    with open(path) as f:
        for line in f:
            data.append(json.loads(line))
    return data

def get_data_path(mode, encoder):
    paths = {}
    if mode == 'train':
        paths['train'] = '../bert_data/gewiki/train.jsonl'
        paths['valid']   = '../bert_data/gewiki/valid.jsonl'
    else:
        paths['test']  = '../bert_data/gewiki/test.jsonl'
    return paths

def get_result_path(save_path):
    dec_path = join(save_path, 'matchsum_hypo')
    ref_path = join(save_path, 'matchhsum_ref')
    os.makedirs(dec_path)
    os.makedirs(ref_path)
    return dec_path, ref_path
