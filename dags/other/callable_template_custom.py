"""
### DAG that uses a callable for a templatable parameter

Also shows the new `skip_when_already_exists` parameter in the TriggerDagRunOperator.
"""

from airflow.decorators import dag, task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.models.baseoperator import chain
from pendulum import datetime


@dag(
    start_date=None,
    schedule=None,
    catchup=False,
    tags=["2-10", "callable for templating", "tdro"],
)
def callable_template_custom():

    @task
    def upstream():
        return "hi"

    def build_conf(context, jinja_env):  # the two kwargs are mandatory
        import json

        with open("include/configuration.json", "r") as file:
            data = json.load(file)
        value = data.get("time_value", None)
        return {"sleep_time": value}

    tdro = TriggerDagRunOperator(
        task_id="tdro",
        trigger_dag_id="tdro_downstream",
        wait_for_completion=True,
        conf=build_conf,
        skip_when_already_exists=True,  # New in 2.10
        execution_date=datetime(2024, 8, 13),
    )

    @task
    def downstream():
        return "bye"

    chain(upstream(), tdro, downstream())


callable_template_custom()
