#! /bin/bash

FILE=$1
ret=$(iconv -t UTF-8 ${FILE} -o ${FILE}-conv)
if [ $? -ne 0 ]; then
        echo "Length ${FILE}-conv:"
        cat ${FILE}-conv | wc -l
        echo "Length ${FILE}"
        cat ${FILE} | wc -l
fi
