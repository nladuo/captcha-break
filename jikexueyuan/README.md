# CSDN Download
CAPTCHA from http://download.csdn.net/
## captcha image
![](./csdn.png)  
## status
building.
## technique
recognize the CAPTCHA by matching the template.
## Steps
### 1.download the captcha and convert the captchas from .gif to .png
``` shell
rm ./downloader/captchas/*
go run ./downloader/downloader.go
cd ./downloader && python ./Gif2PngConverter.py && cd ..
```
### 2.get the templates of each letter by using software like Photoshop.  
You can check the result at [./recognizer/templates](./recognizer/templates)

### 3.test the recognizer
building...
