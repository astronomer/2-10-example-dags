"""
### Basic Dataset schedule - Upstream 2

This DAG shows a basic Dataset implementation for reference.

It produces an update to the s3://basic-datasets/output_2.txt file.
"""

from airflow.decorators import dag, task
from airflow.models.dataset import Dataset
from pendulum import datetime
import logging

t_log = logging.getLogger("airflow.task")


@dag(
    start_date=datetime(2024, 8, 1),
    schedule=None,
    catchup=False,
    doc_md=__doc__,
    tags=["2-10", "Datasets", "Basic Dataset Schedule"],
)
def basic_dataset_schedule_upstream_2():

    @task(outlets=[Dataset("s3://basic-datasets/output_2.txt")])
    def write_to_s3():
        t_log.info("I'm pretending to write a txt file to S3.")

    write_to_s3()


basic_dataset_schedule_upstream_2()
