import nltk
import json
import pandas as pd
from prepro import data_builder
from train import test_from_outside
from others.logging import logger, init_logger


class clsprops:
    def __init__(self, data):
        self.__dict__ = data


def data_prep_for_BertSum(texts: list, save_path: str) -> None:
    print(f"Sentence splitting, tokenizing and converting to json...")
    dataset_json = []
    language: str = 'german'
    for text in texts:
        src_tokens = []
        tgt_tokens = []

        src_sentences = nltk.sent_tokenize(text, language)
        for sent in src_sentences:
            src_tokens.append(nltk.word_tokenize(sent, language))

        dataset_json.append({'src': src_tokens, 'tgt': tgt_tokens})

    if (len(dataset_json) > 0):
        pt_file = "{:s}/{:s}.{:d}.json".format("../json_data/temp", "test", 0)
        with open(pt_file, 'w') as save:
            save.write(json.dumps(dataset_json))


def summarize_with_bertsum(texts: list) -> list:
    if (not len(texts)):
        return []

    json_path = '../json_data/temp'
    bert_path = '../bert_data/temp'
    logs_path = '../logs/temp'
    results_path = '../results/temp'
    bert_model_path = '../models/mlsum/mlsum_bertsum_model_step_45000.pt'

    init_logger(logs_path)

    # Data Preparation
    data_prep_for_BertSum(texts, json_path)

    # Data Preprocessing
    prepro_args = {'dataset': '', 'raw_path': json_path, 'save_path': bert_path, 'oracle_mode': 'greedy', 'n_cpus': 4,
                   'log_file': logs_path, 'min_nsents': 3, 'max_nsents': 100, 'min_src_ntokens': 5,
                   'max_src_ntokens': 200, 'lower': True}
    data_builder.format_to_bert(clsprops(prepro_args))

    # Predict
    test_args = {'visible_gpus': 0, 'bert_config_path': '../bert_config_uncased_base.json', 'temp_dir': 'temp',
                 'encoder': 'classifier', 'param_init': 0, 'param_init_glorot': True, 'bert_data_path': bert_path,
                 'batch_size': 1000, 'accum_count': 1, 'world_size': 1, 'model_path': 'models/', 'report_every': 1,
                 'save_checkpoint_steps': 5, 'test_from': bert_model_path, 'log_file': logs_path,
                 'result_path': results_path, 'use_interval': True, 'hidden_size': 128, 'ff_size': 512,
                 'heads': 4, 'inter_layers': 2, 'rnn_size': 512, 'dropout': 0.1, 'optim': 'adam', 'lr': 1, 'beta1': 0.9,
                 'beta2': 0.999, 'decay_method': '', 'warmup_steps': 8000, 'max_grad_norm': 0, 'recall_eval': False,
                 'train_steps': 1000, 'gpu_ranks': '0', 'dataset': '', 'seed': 666, 'test_all': False, 'train_from': '',
                 'report_rouge': False, 'block_trigram': True}
    test_from_outside(clsprops(test_args))