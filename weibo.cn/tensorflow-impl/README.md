## Weibo.cn tensorflow-trainer

use tensorflow to train the weibo.cn dataset.

## Note
This is just a demo to train the weibo.cn dataset.

## Dependancy
- Tensorflow-1.0
- scikit-learn-0.18
- pillow

## Train Step
1. load the models
``` sh
python load_models.py
```

2. check the dataset
``` sh
python check_dataset.py
```

3. train
``` sh
python train.py
```

## Recognize Step
1. compile the captcha spliter written in c++(require opencv & cmake)
``` sh
cd spliter_for_tf   # enter the spliter directory
cmake . && make     # compile the spliter
cd ..               # back to tenforflow-impl dir
```

2. run the run_recoginze.sh
``` sh
bash run_recognize.sh test.png
```