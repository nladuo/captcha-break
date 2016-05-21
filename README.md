# captcha-break
captcha break based on opencv2, tesseract-ocr and some machine learning algorithm.

## basic
#### captcha image
![](./basic/basic.jpg)
#### status 
finished.  
#### technique
use tesseract-ocr directly.  

## csdn_download
#### captcha image
type1: ![](./csdn_download/csdn1.png)  
type2: ![](./csdn_download/csdn2.png)
#### status
building...
#### technique
use vertical projection to split the word, and knn to recognize the word.

## weibo.cn
#### captcha image
![](./weibo.cn/weibo.cn.png)
#### status 
building...  
#### technique
use some computer vision to clean the noise, 
vertical projection to split the word, and cnn to train the dataset.


