#-------------------------------------------------
#
# Project created by QtCreator 2016-05-14T13:02:32
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = weibo_captcha_break
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    captcha_utils.cpp \
    histogram1d.cpp \
    harris_detector.cpp

HEADERS  += mainwindow.h \
    captcha_utils.h \
    histogram1d.h \
    harris_detector.h

FORMS    += mainwindow.ui


INCLUDEPATH += /usr/local/include \
                /usr/local/include/opencv \
                /usr/local/include/opencv2

LIBS += /usr/local/lib/libopencv_highgui.dylib \
        /usr/local/lib/libopencv_core.dylib    \
        /usr/local/lib/libopencv_imgproc.dylib
