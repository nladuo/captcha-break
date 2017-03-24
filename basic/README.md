# basic
The simplest captcha breaking.

## The Captcha Image
![](./basic.jpg)

## Status
finished.  

## Technique
use tesseract-ocr directly.

## Steps
### 1.build
``` shell
cmake . && make
```
### 2.recognize
``` shell
./recognizer basic.jpg
./recognizer test1.jpg
./recognizer test2.jpg
./recognizer test3.jpg
```
