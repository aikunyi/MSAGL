import argparse
import os
import torch
from exp.exp_classification import Exp_Classification
import random
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TimesNet")

    # basic config
    parser.add_argument("--task_name", type=str, default="classification")
    parser.add_argument("--is_training", type=int, default=1, help="status")
    parser.add_argument("--model_id", type=str, default="APAVA-Subject", help="model id")
    parser.add_argument("--model", type=str, default="MedGNN", help="[MedGNN, Medformer, iTransformer]")
    parser.add_argument('--checkpoints', type=str, default='./checkpoints/', help='location of model checkpoints')

    parser.add_argument("--data", type=str, default="APAVA", help="dataset type")
    parser.add_argument("--root_path", type=str, default="../dataset/APAVA", help="root path of the data file")
    parser.add_argument("--freq", type=str, default="h",
        help="freq for time features encoding, options:[s:secondly, t:minutely, h:hourly, d:daily, b:business days, w:weekly, m:monthly], you can also use more detailed freq like 15min or 3h")

    parser.add_argument("--d_model", type=int, default=256, help="dimension of model")
    parser.add_argument("--d_ff", type=int, default=512, help="dimension of fcn")
    parser.add_argument("--n_heads", type=int, default=8, help="num of heads")
    parser.add_argument("--e_layers", type=int, default=4, help="num of encoder layers")
    parser.add_argument("--d_layers", type=int, default=1, help="num of decoder layers")
    parser.add_argument("--dropout", type=float, default=0.1, help="dropout")
    parser.add_argument("--embed", type=str, default="timeF", help="time features encoding, options:[timeF, fixed, learned]")
    parser.add_argument("--activation", type=str, default="gelu", help="activation")
    parser.add_argument("--output_attention", action="store_true", help="whether to output attention in encoder")

    parser.add_argument("--patch_len_list", type=str, default="2,2,2,4,4,4,16,16,16,16,32,32,32,32,32", help="a list of patch len used in Medformer")
    parser.add_argument("--single_channel", action="store_true", default=False, help="whether to use single channel patching for Medformer")
    parser.add_argument("--augmentations", type=str, default="none,drop0.35",
                        help="a comma-seperated list of augmentation types (none, jitter or scale). Append numbers to specify the strength of the augmentation, e.g., jitter0.1")

    # MedGNN
    parser.add_argument('--resolution_list', type=str, default="2,4,6,8")
    parser.add_argument('--nodedim', type=int, default=10)

    # optimization
    parser.add_argument("--num_workers", type=int, default=10, help="data loader num workers")
    parser.add_argument("--itr", type=int, default=1, help="experiments times")
    parser.add_argument("--train_epochs", type=int, default=10, help="train epochs")
    parser.add_argument("--batch_size", type=int, default=64, help="batch size of train input data")
    parser.add_argument("--patience", type=int, default=3, help="early stopping patience")
    parser.add_argument("--learning_rate", type=float, default=0.0001, help="optimizer learning rate")
    parser.add_argument("--des", type=str, default="test", help="exp description")
    parser.add_argument("--loss", type=str, default="MSE", help="loss function")
    parser.add_argument("--lradj", type=str, default="type1", help="adjust learning rate")
    parser.add_argument("--use_amp", action="store_true", default=False, help="use automatic mixed precision training")
    parser.add_argument("--swa", action="store_true", default=False, help="use stochastic weight averaging")

    # GPU
    parser.add_argument("--use_gpu", type=bool, default=True, help="use gpu")
    parser.add_argument("--gpu", type=int, default=0, help="gpu")
    parser.add_argument("--use_multi_gpu", help="use multiple gpus", default=False)
    parser.add_argument("--devices", type=str, default="0, 1, 2, 3", help="device ids of multiple gpus")

    args = parser.parse_args()
    args.use_gpu = True if torch.cuda.is_available() and args.use_gpu else False

    if args.use_gpu and args.use_multi_gpu:
        args.devices = args.devices.replace(" ", "")
        device_ids = args.devices.split(",")
        args.device_ids = [int(id_) for id_ in device_ids]
        args.gpu = args.device_ids[0]

    print("Args in experiment:")
    print(args)

    if args.task_name == "classification":
        Exp = Exp_Classification

    if args.is_training:
        for ii in range(args.itr):
            seed = 41 + ii
            random.seed(seed)
            os.environ["PYTHONHASHSEED"] = str(seed)
            np.random.seed(seed)
            torch.manual_seed(seed)
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            # comment out the following lines if you are using dilated convolutions, e.g., TCN
            # otherwise it will slow down the training extremely
            torch.backends.cudnn.benchmark = False
            torch.backends.cudnn.deterministic = True


            # setting record of experiments
            args.seed = seed
            setting = "{}_{}_{}_dm{}_df{}_nh{}_el{}_res{}_node{}_seed{}_bs{}_lr{}".format(
                args.model_id,
                args.model,
                args.data,
                args.d_model,
                args.d_ff,
                args.n_heads,
                args.e_layers,
                args.resolution_list,
                args.nodedim,
                args.seed,
                args.batch_size,
                args.learning_rate,
            )

            exp = Exp(args)  # set experiments
            print(
                ">>>>>>>start training : {}>>>>>>>>>>>>>>>>>>>>>>>>>>".format(setting)
            )
            exp.train(setting)

            print(
                ">>>>>>>testing : {}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<".format(setting)
            )
            exp.test(setting)
            torch.cuda.empty_cache()
    else:
        for ii in range(args.itr):
            seed = 41 + ii
            random.seed(seed)
            os.environ["PYTHONHASHSEED"] = str(seed)
            np.random.seed(seed)
            torch.manual_seed(seed)
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            # comment out the following lines if you are using dilated convolutions
            # otherwise it will slow down the training extremely
            torch.backends.cudnn.benchmark = False
            torch.backends.cudnn.deterministic = True

            args.seed = seed
            setting = "{}_{}_{}_dm{}_df{}_nh{}_el{}_res{}_node{}_seed{}_bs{}_lr{}".format(
                args.model_id,
                args.model,
                args.data,
                args.d_model,
                args.d_ff,
                args.n_heads,
                args.e_layers,
                args.resolution_list,
                args.nodedim,
                args.seed,
                args.batch_size,
                args.learning_rate,
            )

            exp = Exp(args)  # set experiments
            print(
                ">>>>>>>testing : {}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<".format(setting)
            )
            exp.test(setting, test=1)
            torch.cuda.empty_cache()
