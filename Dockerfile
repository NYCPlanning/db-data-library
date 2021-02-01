FROM osgeo/gdal:ubuntu-small-3.2.1

COPY . /library/

WORKDIR /library/

RUN apt update && apt install -y python3-pip python3-distutils

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

RUN . $HOME/.poetry/env;\
    poetry config virtualenvs.create false --local;\
    poetry install
