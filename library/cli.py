import os
import time
from typing import Optional

import typer

from . import aws_access_key_id, aws_s3_bucket, aws_s3_endpoint, aws_secret_access_key
from .archive import Archive
from .s3 import S3

app = typer.Typer()

# fmt: off
@app.command()
def archive(
    path: str = typer.Option(None, "--path", "-f", help="Path to config yml"),
    output_format: str = typer.Option("pgdump", "--output-format", "-o", help="csv, geojson, shapefile, pgdump and postgres"),
    push: bool = typer.Option(False, "--s3", "-s", help="Push to s3"),
    clean: bool = typer.Option(False, "--clean", "-c", help="Remove temporary files"),
    latest: bool = typer.Option(False, "--latest", "-l", help="Tag with latest"),
    name: str = typer.Option(None, "--name", "-n", help="Name of the dataset, if supplied, \"path\" will ignored"),
    compress: bool = typer.Option(False, "--compress", help="Compress output"),
    inplace: bool = typer.Option(False, "--inplace", help="Only keeping zipped file"),
    postgres_url: str = typer.Option(None, "--postgres-url", help="Postgres connection url"),
    version: str = typer.Option(None, "--version", "-v", help="Custom version input"),
) -> None:
# fmt: on
    """
    Archive a dataset from source to destination
    """
    if not name and not path:
        message = typer.style("\nPlease specify dataset NAME or PATH to configuration\n", fg=typer.colors.RED)
        typer.echo(message)
    else:
        a = Archive()
        a(
            path=path,
            output_format=output_format,
            push=push,
            clean=clean,
            latest=latest,
            name=name,
            compress=compress,
            inplace=inplace,
            postgres_url=postgres_url,
            version=version,
        )

# fmt: off
@app.command()
def show(
    name: str,
    uploaded: bool = typer.Option(False, "--uploaded", "-u", help="Show upload dates for each file")
) -> None:
# fmt: on
    """
    Display files available in the s3 library for a given dataset. Option to display latest upload
    date for each file.
    """
    s3 = S3(aws_access_key_id, aws_secret_access_key, aws_s3_endpoint, aws_s3_bucket)
    if not uploaded:
        keys = s3.ls(f"datasets/{name}/")
        message = "\n".join([k.replace(f"datasets/{name}/", "") for k in keys])
        typer.echo(message)
    if uploaded:
        keys = s3.ls(f"datasets/{name}/", detail=True)
        upload_dates = {k['Key'].replace(f"datasets/{name}/", ""):str(k['LastModified']) for k in keys}
        message = "\n".join([f"File: {v} \t Last upload date: {d}" for v, d in upload_dates.items()])
        typer.echo(message)

def run() -> None:
    """Run commands."""
    app()
