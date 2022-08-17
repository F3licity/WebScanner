FROM python:3.8

COPY ./webscanner.py ./
COPY ./slackHandler.py ./
COPY ./requirements.txt ./

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "./webscanner.py" ]