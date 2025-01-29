# Subject-based
# APAVA Dataset
python \
  -u run.py \
  --task_name classification \
  --is_training 1 \
  --root_path ../dataset/APAVA/ \
  --model_id APAVA-Subject \
  --model MedGNN \
  --data APAVA \
  --e_layers 4 \
  --batch_size 64 \
  --d_model 256 \
  --d_ff 512 \
  --n_heads 8 \
  --resolution_list 2,4,6,8 \
  --nodedim 10 \
  --augmentations none,drop0.35 \
  --des 'Exp' \
  --itr 1 \
  --learning_rate 0.0001 \
  --train_epochs 10 \
  --patience 3