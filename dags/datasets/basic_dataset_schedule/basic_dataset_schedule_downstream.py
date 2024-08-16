"""
### Basic Dataset schedule - Downstream

This DAG shows a basic Dataset implementation for reference.

It is scheduled to run on either, s3://basic-datasets/output_2.txt
receiving an update or both, s3://basic-datasets/output_1.txt and 
s3://basic-datasets/output_3.txt
having been updated.
"""

from airflow.decorators import dag, task
from airflow.models.dataset import Dataset
from pendulum import datetime
import logging

t_log = logging.getLogger("airflow.task")


@dag(
    start_date=datetime(2024, 8, 1),
    schedule=(
        (
            Dataset("s3://basic-datasets/output_1.txt")
            & Dataset("s3://basic-datasets/output_3.txt")
        )
        | Dataset("s3://basic-datasets/output_2.txt")
    ),
    catchup=False,
    doc_md=__doc__,
    tags=["2-10", "Datasets", "Basic Dataset Schedule"],
)
def basic_dataset_schedule_downstream():

    @task(outlets=[Dataset("s3://basic-datasets/combined_outputs.txt")])
    def combine():
        t_log.info("I pretend to create a combined dataset!")

    combine()


basic_dataset_schedule_downstream()
