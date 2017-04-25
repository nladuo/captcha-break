# Weibo.cn
CAPTCHA from http://login.weibo.cn/login/
## The Captcha Image
![](../weibo.cn.png)

## Status
finshied.

## Enviorment
Programing Language: C++  
Library: opencv2 + libboost

## Technique
use some computer vision algorithm to clean the peper noise and noise line,
vertical projection to split the word, and CNN to train the dataset.

## Steps
### 1.Download some captchas.
now is unavailable, see the backup at [captchas_backup.zip](../captchas_backup.zip).
### 2.Split the letters from every captcha.
``` shell
cd ./spliter && cmake . && make
mkdir dataset
./spliter
```
### 3. Recognize the letters by human.
You can check the results in [./trainer/training_set.zip](./trainer/training_set.zip)
``` shell
cd ./trainer/
unzip training_set.zip
```
### 4. Train the dataset.
```
cmake . && make
./trainer
mv ./weibo.cn-nn-weights ../recognizer/
```
### 5. Test the recognizer
```
cd ./recognizer && cmake . && make
./recognizer test1.png
./recognizer test2.png
./recognizer test3.png
./recognizer test4.png
```

## About the Accuracy
The accuracy is about 60%.
