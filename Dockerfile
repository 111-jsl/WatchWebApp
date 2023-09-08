# app/Dockerfile

FROM python:3.9-slim

WORKDIR /watch


# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     software-properties-common \
#     && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 config set global.index-url http://mirrors.aliyun.com/pypi/simple/
RUN pip3 config set global.trusted-host mirrors.aliyun.com 

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "首页.py", "--server.port=8501", "--server.address=0.0.0.0"]