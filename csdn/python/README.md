# CSDN Download
CAPTCHA from http://download.csdn.net/

## The Captcha image
![](../csdn.png)  

## Status
finished.

## Enviorment
Programing Language: Python2.7  
Library: Pillow + scikit-learn-0.18

## Technique
split the letter averagely, and use KNN to recognize every letter.

## Steps
### 1.Download some captchas.
``` shell
cd ./downloader
python downloader.py
```
### 2.Split the letters from captchas.  
``` shell
cd ./spliter
python spliter.py
```
### 3.Recognize the letters by human, create the dataset.  
You can check the result at [./recognizer/dataset](./recognizer/dataset)

### 4.Test the recognizer.
```
cd ./recognizer
python recognizer.py test1.png
python recognizer.py test2.png
python recognizer.py test3.png
python recognizer.py test4.png
```
