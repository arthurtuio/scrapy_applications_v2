FROM python:3.8-buster

RUN apt-get update -y \
    && apt-get install -y python3-dev python3-pip build-essential \
    && apt-get install gcc -y \
    && apt-get clean

COPY requirements.txt /requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# RUN mkdir -p /src

CMD [ "streamlit","run", "main_page.py" ]

#FROM phusion/baseimage:master
#
#RUN sed 's/main$/main universe/' -i /etc/apt/sources.list && \
#    apt-get update && apt-get install -y software-properties-common && \
#    add-apt-repository ppa:webupd8team/java -y && \
#    apt-get update && \
#    echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections && \
#    apt-get install -y oracle-java8-installer libxext-dev libxrender-dev libxtst-dev git
#
#COPY requirements.txt /tmp/
#RUN set -ex \
#    && buildDeps=' \
#        python3 \
#        python3-dev \
#        libkrb5-dev \
#        libsasl2-dev \
#        libssl-dev \
#        libffi-dev \
#        build-essential \
#        libblas-dev \
#        liblapack-dev \
#        libpq-dev \
#        python3-setuptools \
#    ' \
#    && apt-get install -y --no-install-recommends \
#        $buildDeps \
#        apt-utils \
#        netcat \
#    && curl "https://bootstrap.pypa.io/get-pip.py" | python3 \
#    && pip install --upgrade pip \
#    && pip install -r /tmp/requirements.txt \
#    && useradd -ms /bin/bash -d /home/developer developer \
#    && apt-get autoremove -y \
#    && apt-get clean \
#    && rm -rf \
#        /var/lib/apt/lists/* \
#        /tmp/* \
#        /var/tmp/* \
#        /usr/share/man \
#        /usr/share/doc \
#        /usr/share/doc-base
#
#EXPOSE 8501
#
#COPY database/entrypoint.sh /entrypoint.sh
#
#ENTRYPOINT ["/entrypoint.sh"]
