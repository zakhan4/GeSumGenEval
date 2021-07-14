import os
import torch
import sys
from torch import nn
from os.path import join
from fastNLP.core.callback import Callback
from fastNLP.core.utils import _model_contains_inner_module


class MyCallback(Callback):
    def __init__(self, args):
        super(MyCallback, self).__init__()
        self.args = args
        self.real_step = 0
    
    def on_train_begin(self):
        if os.path.exists(os.path.expanduser(self.args.train_from)):
            states = torch.load(self.args.train_from)
            model = self.model
            if _model_contains_inner_module(model):
                model = model.module
            model.load_state_dict(states['model'])
            self.optimizer.load_state_dict(states['optimizer'])
            self.trainer.epoch = states['epoch'] 
            self.trainer.step = states['step']
            self.real_step = int(states['step'] / self.update_every)
            if 'best_dev_epoch' in states:
                self.trainer.best_dev_perf = states['best_dev_perf']
                self.trainer.best_dev_epoch = states['best_dev_epoch']
                self.trainer.best_dev_step = states['best_dev_step']
                self.trainer.best_metric_indicator = states['best_metric_indicator']
            print("Load checkpoint from {}".format(os.path.expanduser(self.args.train_from)))

    def on_valid_begin(self):
        with open(join(self._trainer.save_path, 'train_info.txt'), 'a') as f:
            print('Current step is: {}'.format(self.step), file=f)

    def on_valid_end(self, eval_result, metric_key, optimizer, is_better_eval):
        states = {}
        model = self.model
        if _model_contains_inner_module(model):
            model = model.module
        states['model'] = {name:param.cpu() for name, param in model.state_dict().items()}
        states['optimizer'] = self.optimizer.state_dict()
        states['epoch'] = self.epoch
        states['step'] = self.step
        if self.trainer.best_dev_epoch is not None:
            states['best_dev_epoch'] = self.trainer.best_dev_epoch
            states['best_dev_perf'] = self.trainer.best_dev_perf
            states['best_dev_step'] = self.trainer.best_dev_step
            states['best_metric_indicator'] = self.trainer.best_metric_indicator
        torch.save(states, self.args.train_from)
        print("Checkpoint:{} has been saved in epoch:{}.".format(self.args.train_from, self.epoch))
        
    def on_step_end(self):
        # warm up
        if self.step % self.update_every == 0 and self.step > 0:
            self.real_step += 1
            cur_lr = self.args.max_lr * 100 * min(self.real_step ** (-0.5), self.real_step * self.args.warmup_steps**(-1.5))
            for param_group in self.optimizer.param_groups:
                param_group['lr'] = cur_lr

            if self.real_step % 1000 == 0:
                self.pbar.write('Current learning rate is {:.8f}, real_step: {}'.format(cur_lr, self.real_step))
    
    def on_epoch_end(self):
        self.pbar.write('Epoch {} is done !!!'.format(self.epoch))
