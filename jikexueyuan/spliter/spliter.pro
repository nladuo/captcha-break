#-------------------------------------------------
#
# Project created by QtCreator 2016-10-05T12:41:11
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = spliter
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    captcha_utils.cpp

HEADERS  += mainwindow.h \
    captcha_utils.h

FORMS    += mainwindow.ui

INCLUDEPATH += /usr/local/include \
                /usr/local/include/opencv \
                /usr/local/include/opencv2

LIBS += /usr/local/lib/libopencv_highgui.so \
        /usr/local/lib/libopencv_core.so    \
        /usr/local/lib/libopencv_imgproc.so \
        /usr/local/lib/libopencv_ml.so
