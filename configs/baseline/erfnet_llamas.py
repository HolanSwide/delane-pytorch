from importmagician import import_from
with import_from('./'):
    # Data pipeline
    from configs.common.datasets.llamas_seg import dataset
    from configs.common.datasets.train_level0_360 import train_augmentation
    from configs.common.datasets.test_360 import test_augmentation

    # Optimization pipeline
    from configs.common.optims.segloss_5class import loss
    from configs.common.optims.sgd05 import optimizer
    from configs.common.optims.ep10_poly_warmup200 import lr_scheduler


train = dict(
    exp_name='erfnet_baseline_llamas',
    workers=10,
    batch_size=20,
    checkpoint=None,
    # Device args
    world_size=0,
    dist_url='env://',
    device='cuda',

    val_num_steps=0,  # Seg IoU validation (mostly useless)
    save_dir='./checkpoints',

    input_size=(360, 640),
    original_size=(717, 1276),
    num_classes=5,
    num_epochs=10,
    collate_fn=None,  # 'dict_collate_fn' for LSTR
    seg=True  # Seg-based method or not
)

test = dict(
    exp_name='erfnet_baseline_llamas',
    workers=10,
    batch_size=80,
    checkpoint='./checkpoints/erfnet_baseline_llamas/model.pt',
    # Device args
    device='cuda',

    save_dir='./checkpoints',

    seg=True,
    gap=1,
    ppl=417,
    thresh=0.3,
    collate_fn=None,  # 'dict_collate_fn' for LSTR
    input_size=(360, 640),
    original_size=(717, 1276),
    max_lane=4,
    dataset_name='llamas'
)

model = dict(
    name='ERFNet',
    num_classes=5,
    dropout_1=0.3,
    dropout_2=0.3,
    pretrained_weights='erfnet_encoder_pretrained.pth.tar',
    lane_classifier_cfg=dict(
        name='EDLaneExist',
        num_output=5 - 1,
        flattened_size=4400,
        dropout=0.3,
        pool='max'
    )
)
