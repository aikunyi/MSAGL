# sample-based
# ADFD Dataset
python \
  -u run.py \
  --task_name classification \
  --is_training 1 \
  --root_path ../dataset/ADFD/ \
  --model_id ADFD-Sample \
  --model MSAGL \
  --data ADFD-Sample \
  --e_layers 6 \
  --batch_size 128 \
  --d_model 256 \
  --d_ff 512 \
  --n_heads 8 \
  --resolution_list 2 \
  --nodedim 10 \
  --augmentations drop0.2 \
  --des 'Exp' \
  --itr 1 \
  --learning_rate 0.0001 \
  --train_epochs 10 \
  --patience 3