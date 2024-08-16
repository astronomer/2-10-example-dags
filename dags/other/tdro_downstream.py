"""
### Downstream DAG for callable_template_custom

Just here as the target for the TDRO, gets sleep time
as conf through it.
"""

from airflow.decorators import dag, task
from airflow.models.param import Param
import time


@dag(
    start_date=None,
    schedule=None,
    catchup=False,
    params={"sleep_time": Param(100, type="number")},
    tags=["2-10", "callable for templating", "tdro"],
)
def tdro_downstream():

    @task
    def sleep(**context):
        my_sleep_time = context["params"]["sleep_time"]
        print(f"Sleeping for {my_sleep_time} seconds!")
        time.sleep(my_sleep_time)
        return "Wake up!"

    sleep()


tdro_downstream()
