# CSDN Download
CAPTCHA from http://download.csdn.net/

## The Captcha image
![](../csdn.png)  

## Status
finished.

## Enviorment
Programing Language: C++  
Library: opencv2 + libboost

## Technique
split the letter averagely, and use KNN to recognize every letter.

## Steps
### 1.Download some captchas.
``` shell
mkdir ./downloader/captchas/
python ./downloader/downloader.py
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
```
