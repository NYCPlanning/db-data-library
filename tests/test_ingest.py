from library.ingest import Ingestor
from sqlalchemy import create_engine
from library import recipe_engine
from . import test_root_path
import os


def test_ingest_translate_csv():
    ingestor = Ingestor()
    ingestor.translate_csv(f"{test_root_path}/data/nypl_libraries.yml", compress=True)
    assert os.path.isfile(
        ".library/datasets/nypl_libraries/20210122/nypl_libraries.csv"
    )


def test_ingest_translate_pgdump():
    ingestor = Ingestor()
    ingestor.translate_pgdump(
        f"{test_root_path}/data/nypl_libraries.yml", compress=True
    )
    assert os.path.isfile(
        ".library/datasets/nypl_libraries/20210122/nypl_libraries.sql"
    )


def test_ingest_translate_shapefile():
    ingestor = Ingestor()
    ingestor.translate_shapefile(f"{test_root_path}/data/nypl_libraries.yml")
    assert os.path.isfile(
        ".library/datasets/nypl_libraries/20210122/nypl_libraries.shp.zip"
    )


def test_ingest_translate_postgres():
    ingestor = Ingestor()
    ingestor.translate_postgres(
        f"{test_root_path}/data/nypl_libraries.yml", recipe_engine
    )
    pg = create_engine(recipe_engine)
    sql = """
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE  table_schema = 'public'
        AND    table_name   = 'nypl_libraries'
    );
    """
    result = pg.execute(sql).fetchall()
    assert result[0][0], "nypl_libraries is not in postgres database yet"

    # Clean up
    if result[0][0]:
        pg.execute("DROP TABLE IF EXISTS nypl_libraries;")
    result = pg.execute(sql).fetchall()
    assert not result[0][0], "clean up failed"
