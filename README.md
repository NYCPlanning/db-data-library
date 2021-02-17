# db-data-library


This is a test adding some additional documentation.

![Docker Image Size (latest by date)](https://img.shields.io/docker/image-size/nycplanning/library)
## Usage:
> Because gdal dependencies are difficult to install, we recommend using this cli with our docker image `nycplanning/library:ubuntu-latest`
1. docker run with `.env` file
> if you have the environmental variables stored in a `.env` file
```bash
docker run --rm --env-file .env \
    nycplanning/library:latest < library ... >
```
> the command can be any of the library commands, e.g.
`library archive --name dcp_commercialoverlay -s -c` & etc
2. docker run with explicit environmental variables
```bash
docker run --rm\
    -e AWS_S3_ENDPOINT=< endpoint >
    -e AWS_SECRET_ACCESS_KEY=< access secret ket >
    -e AWS_ACCESS_KEY_ID=< access key id >
    -e AWS_S3_BUCKET=< bucket name >
    nycplanning/library:latest < library ... >
```

## Dev Instructions:
1. Make sure you have GDAL installed (we are using version `3.2.1+dfsg-1+b1`)
```bash
sudo apt install -y gdal-bin libgdal-dev python3-gdal
```
2. then install poetry
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
```
3. Use poetry to install dependencies `poetry install`
4. Install pre-commit `poetry run pre-commit install`
5. Check out what's available via the cli `poetry run library --help`
6. To add/update documentation, run `poetry run pdoc -o docs --html library`

## Testing:

To test all functions within a script:
`poetry run pytest tests/{test script}.py -s`

To test a specific function:
`poetry run pytest tests/{test script}.py::{test name} -s`
> note the `-s` flag is optional, it allows print output (via stdout) to be included in the test output, otherwise it is ignored
