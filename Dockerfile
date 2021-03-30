FROM python:3.8-buster

RUN apt-get update -y \
    && apt-get install -y python3-dev python3-pip build-essential \
    && apt-get install gcc -y \
    && apt-get clean

COPY requirements.txt /scrapy_applications_v2/requirements.txt
COPY main_page.py /scrapy_applications_v2/main_page.py

ADD application /scrapy_applications_v2/application/
ADD project_folder /scrapy_applications_v2/project_folder/

WORKDIR /scrapy_applications_v2/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["streamlit", "run", "main_page.py"]
