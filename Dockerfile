FROM osgeo/gdal:ubuntu-small-3.2.1

COPY . /library/

WORKDIR /library/

RUN apt update && apt install -y python3-pip python3-distutils

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_VERSION=1.1.6 python3 -
ENV PATH="${PATH}:/root/.poetry/bin"
RUN poetry export -f requirements.txt --output requirements.txt;\
    pip install -r requirements.txt