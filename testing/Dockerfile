FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev 
RUN pip3 install --upgrade pip

RUN pip3 install presidio-anonymizer
RUN pip3 install presidio-analyzer
RUN pip3 install numpy
RUN pip3 install geopy
RUN pip3 install spacy
RUN python3 -m spacy download es_core_news_sm


RUN useradd app
USER app
