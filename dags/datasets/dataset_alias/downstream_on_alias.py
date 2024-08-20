"""
### Dataset Alias implementation - Downstream on Alias
"""

from airflow.decorators import dag, task
from airflow.datasets import DatasetAlias
from pendulum import datetime
import logging
import time

t_log = logging.getLogger("airflow.task")

my_alias_name = "my_alias_6"


@dag(
    start_date=datetime(2024, 8, 1),
    schedule=[DatasetAlias(my_alias_name)],
    catchup=False,
    doc_md=__doc__,
    tags=["2-10", "Datasets", "Dataset Alias", "demo"],
)
def downstream_on_alias():

    @task
    def downstream():
        time.sleep(10)
        pass

    downstream()


downstream_on_alias()
