"""
### Run if/ skip if example DAG
"""

from airflow.decorators import dag, task
from pendulum import datetime


@dag(
    start_date=datetime(2024, 8, 1),
    schedule=None,
    catchup=False,
    tags=["2-10", "Task Flow API", "run_if/skip_if", "demo"],
)
def run_if_skip_if_example():
    @task.run_if(lambda context: context["task_instance"].task_id.endswith("_do_run"))
    @task
    def say_hello():
        return "hello!"

    say_hello.override(task_id="say_hi_do_run")()
    say_hello.override(task_id="say_hi_1234")()


    def skip_decision(context):
        task_id_ending_to_skip = "_skip_me"
        return context["task_instance"].task_id.endswith(task_id_ending_to_skip)

    @task.skip_if(skip_decision)
    @task
    def say_bye():
        return "hello!"

    say_bye.override(task_id="say_bye_skip_me")()
    say_bye.override(task_id="say_bye_1234")()


run_if_skip_if_example()
