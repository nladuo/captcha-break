# Weibo.cn
CAPTCHA from http://login.weibo.cn/login/
## captcha image
![](./weibo.cn.png)
## status
building...  
## technique
use some computer vision algorithm to clean the peper noise and noise line, 
vertical projection to split the word, and cnn to train the dataset.
## Steps
### 1.Download some captchas.
``` shell
mkdir ./downloader/captchas/
python ./downloader/downloader.py
```
### 2.Split the letters from every captcha.
``` shell
cd ./spliter && cmake . && make
mkdir dataset
./spliter
```
### 3. Recognize the letters by human.
You can check the result in [./trainer/training_set.zip](./trainer/training_set.zip)
``` shell
cd ..
unzip training_set.zip
```
### 4. Train the dataset.
...