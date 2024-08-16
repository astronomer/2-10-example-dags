"""
### Branch directly to a task group

"""

from airflow.decorators import dag, task_group, task
from airflow.models.baseoperator import chain
from pendulum import datetime


@dag(
    start_date=datetime(2024, 8, 1),
    schedule=None,
    catchup=False,
    tags=["2-10", "Branching"],
)
def task_group_branching():

    @task.branch
    def upstream_task():
        return "my_task_group"

    @task_group
    def my_task_group():

        @task
        def t1():
            return "hi"

        t1()

        @task
        def t2():
            return "hi"

        t2()

    @task
    def outside_task():
        return "hi"

    chain(upstream_task(), [my_task_group(), outside_task()])


task_group_branching()
