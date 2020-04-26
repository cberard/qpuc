#!/bin/bash
#Clara fav script

docker build -t qpuc-image . && docker run -it --name qpuc-container -p 80:80 qpuc-imgae:latest