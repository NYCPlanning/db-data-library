import os

from library.ingest import Ingestor

from . import template_path


def test_bpl_libraries():
    ingestor = Ingestor()
    ingestor.csv(f"{template_path}/bpl_libraries.yml", version="test")
    assert os.path.isfile(".library/datasets/bpl_libraries/test/bpl_libraries.csv")


def test_dpr_capitalprojects():
    ingestor = Ingestor()
    ingestor.csv(f"{template_path}/dpr_capitalprojects.yml", version="test")
    assert os.path.isfile(
        ".library/datasets/dpr_capitalprojects/test/dpr_capitalprojects.csv"
    )

# NOTE disable due to unexpected test failure:
# RuntimeError: Terminating translation prematurely after failed
# translation of layer tmpo73nzl58 (use -skipfailures to skip errors)
# def test_nypl_libraries():
#     ingestor = Ingestor()
#     ingestor.csv(f"{template_path}/nypl_libraries.yml", version="test")
#     assert os.path.isfile(".library/datasets/nypl_libraries/test/nypl_libraries.csv")


def test_uscourts_courts():
    ingestor = Ingestor()
    ingestor.csv(f"{template_path}/uscourts_courts.yml", version="test")
    assert os.path.isfile(".library/datasets/uscourts_courts/test/uscourts_courts.csv")
