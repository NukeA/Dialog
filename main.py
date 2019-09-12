import pickle

import sentencepiece as spm
import torch
import torch.optim as optim
from torch.utils.data import DataLoader

from config import Config
from nn import Seq2SeqModel, LabelSmoothing, get_optimizer
from utils import DialogDataset, train, seed_everything

if __name__ == '__main__':

    seed_everything(Config.seed)

    start_epoch = 0

    model = Seq2SeqModel(bert_model_dir=Config.bert_path).cuda()
    sp = spm.SentencePieceProcessor()
    sp.Load(Config.sp_path)

    criterion = LabelSmoothing(len(sp), pad_id=Config.pad_id, smoothing=Config.smoothing)
    _opt = optim.Adam(model.parameters(), lr=0, betas=(0.9, 0.98), eps=1e-9)
    optimizer = get_optimizer(_opt, factor=Config.factor, warmup=Config.warmup)

    if Config.load:
        save_obj = torch.load(f'{Config.output_dir}/{Config.fn}.pth')
        model.load(save_obj['model'])
        # optimizer.load(save_obj['opt'], save_obj['param'])
        # start_epoch = save_obj['epoch']

    with open(Config.train_data_path, 'rb') as f:
        train_data = pickle.load(f)
    dataset = DialogDataset(train_data)
    loader = DataLoader(dataset, batch_size=Config.batch_size, shuffle=True)

    train(Config, model, optimizer, criterion, loader,
          sp, start_epoch)
