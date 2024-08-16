from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from pendulum import datetime

from include.custom_deferrable_operator import MyDeferrableOperator


@dag(
    start_date=datetime(2024, 8, 1),
    schedule=None,
    catchup=False,
    tags=["2-10", "Deferrable Operators"],
)
def direct_deferrable():

    @task 
    def upstream():
        return "hi"

    never_meet_a_worker = MyDeferrableOperator(
        task_id="never_meet_a_worker",
        poke_interval=20,
        wait_for_completion=True,
        deferrable=True
    )

    @task
    def downstream():
        return "hi"
    

    chain(upstream(), never_meet_a_worker, downstream())


direct_deferrable()