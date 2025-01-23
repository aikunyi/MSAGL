from data_provider.data_loader import (
    APAVALoader,
    ADFDLoader,
    ADFDDependentLoader,
    TDBRAINLoader,
    PTBLoader,
    PTBXLLoader,
)
from data_provider.uea import collate_fn
from torch.utils.data import DataLoader

data_dict = {
    # following used in our paper
    "APAVA": APAVALoader,  # dataset APAVA
    "TDBRAIN": TDBRAINLoader,  # dataset TDBRAIN
    "ADFD": ADFDLoader,  # dataset ADFD
    "ADFD-Sample": ADFDDependentLoader,  # dataset ADFD with sample-based setup
    "PTB": PTBLoader,  # dataset PTB
    "PTB-XL": PTBXLLoader,  # dataset PTB-XL
}


def data_provider(args, flag):
    Data = data_dict[args.data]
    timeenc = 0 if args.embed != "timeF" else 1

    if flag == "test":
        shuffle_flag = False
        drop_last = True
        if args.task_name == "classification":
            batch_size = args.batch_size
        else:
            batch_size = 1  # bsz=1 for evaluation
        freq = args.freq
    else:
        shuffle_flag = True
        drop_last = True
        batch_size = args.batch_size  # bsz for train and valid
        freq = args.freq

    if args.task_name == "classification":
        drop_last = False
        data_set = Data(
            root_path=args.root_path,
            flag=flag,
        )

        data_loader = DataLoader(
            data_set,
            batch_size=batch_size,
            shuffle=shuffle_flag,
            num_workers=args.num_workers,
            drop_last=drop_last,
            collate_fn=lambda x: collate_fn(
                x, max_len=args.seq_len
            ),  # only called when yeilding batches
        )
        return data_set, data_loader