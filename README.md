# MedGNN (WWW 2025)

The repo is the official implementation for the paper: "Towards Multi-resolution Spatiotemporal Graph Learning for Medical Time Series Classification".

## Getting Started

### Environment Requirements

To get started, ensure you have conda installed on your system and follow these steps to set up the environment:

```
conda create -n MedGNN python=3.9
conda activate MedGNN
pip install -r requirements.txt
```

## Datasets

APAVA dataset: https://drive.google.com/file/d/1FKvUnB8qEcHng7J9CfHaU7gqRLGeS7Ea/view?usp=drive_link.

ADFD dataset: https://drive.google.com/file/d/1QcX_M58IQUBn3lDBlVVL0SDN7_QI1vWe/view.

PTB dataset: https://drive.google.com/file/d/14fBIXc2gSHm00wLaejNIsPgitc-wZdXu/view.

PTB-XL dataset: https://drive.google.com/file/d/1whskRvTZUNb1Qph2SeXEdpcU2rQY0T1E/view.

## Training Example

You can reproduce the experiment results as the following examples:

```
bash ./scripts/ADFD_Sample.sh
bash ./scripts/APAVA_Subject.sh
```


## Acknowledgement

We appreciate the following GitHub repositories for providing valuable code bases and datasets:

Time-Series-Library: https://github.com/thuml/Time-Series-Library

Medformer: https://github.com/DL4mHealth/Medformer

iTransformer: https://github.com/thuml/iTransformer

PatchTST: https://github.com/yuqinie98/PatchTST

FEDformer: https://github.com/MAZiqing/FEDformer

Crossformer: https://github.com/Thinklab-SJTU/Crossformer

FourierGNN: https://github.com/aikunyi/FourierGNN

CrossGNN: https://github.com/hqh0728/CrossGNN

TodyNet: https://github.com/liuxz1011/TodyNet

SimTSC: https://github.com/daochenzha/SimTSC