# SubMail
CAPTCHA from http://submail.cn/sms
## The Captcha Image
![](../submail.png)  

## Status
finished.

## Technique
split the letters with findCountours, and use template to recognize every letter.

## Enviorment
Programing Language: C++  
Library: opencv2 + libboost

## Steps
### 1.Download some captchas.
``` shell
cd ./downloader/
python downloader.py
```
### 2.Split the letters from captchas.  
``` shell
cd ./spliter && cmake . && make
mkdir letters
./spliter
```
### 3.Recognize the letters by human, create the dataset.  
You can check the result at [./recognizer/dataset](./recognizer/dataset)

### 4.Test the recognizer.
```
cd ./recognizer && cmake . && make
./recognizer test1.png
./recognizer test2.png
./recognizer test3.png
./recognizer test4.png
./recognizer test5.png
```
