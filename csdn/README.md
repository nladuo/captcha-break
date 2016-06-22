# CSDN Download
CAPTCHA from http://download.csdn.net/
## captcha image
![](./csdn.png)  
## status
finished.
## technique
split the letter averagely, and use KNN to recognize the letter.
## Steps
### 1.download the captcha  
``` shell
mkdir ./downloader/captchas/
python ./downloader/downloader.py
```
### 2.split the letter from captcha  
``` shell
cd ./spliter && cmake . && make
mkdir letters
./spliter
```
### 3.recognize the letter by human, create the dataset.  
You can check the result at [./recognizer/dataset](./recognizer/dataset)

### 4.test the recognizer
```
cd ./recognizer && cmake . && make
./recognizer test1.png
./recognizer test2.png
./recognizer test3.png
./recognizer test4.png
```
