#  Copyright (c) 2019. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

class Config:
    bos_id = 4
    eos_id = 5
    pad_id = 3
    start_id = 7

    n_epoch = 20
    batch_size = 256
    max_len = 12

    smoothing = 0.1
    factor = 2
    warmup = 4000

    output_dir = './models'
    fn = 'ckpt'

    load = False

    bert_path = './pretrained'
    sp_path = './pretrained/wiki-ja.model'

    train_data_path = './data/txt_pkl/train_data_10.pkl'
