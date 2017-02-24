FROM python:3.6.0
MAINTAINER Oliver Steele <steele@osteele.com>

RUN pip install pytest

RUN mkdir -p /src
COPY setup.py /src/

WORKDIR /src
RUN pip install -e .

ENTRYPOINT ["python", "setup.py", "test"]
