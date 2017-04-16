#!/usr/bin/env bash

if [ x$1 != x ]
then
    ./spliter_for_tf/spliter_for_tf $1
    echo -n "Result:"
    for ((i=0; i<4; ++i))
    do
        ./recognize.py $i".png" 2>/tmp/recoginze_warning.log   # ignore tensorflow warning
        rm $i".png"
    done
    echo ""
else
    echo "Usage: ./run_recognize.sh [image_path]"
fi


