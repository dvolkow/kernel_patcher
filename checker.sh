#! /bin/bash

FILE=$1
ret=$(iconv -t UTF-8 ${FILE} -o ${FILE}-conv)
if [ $? -ne 0 ]; then
        cat ${FILE}-conv | wc -l
fi
