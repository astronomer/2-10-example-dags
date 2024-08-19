"""
### Emitting Lineage from a Hook
"""

from airflow.decorators import dag, task
from airflow.datasets import Dataset
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from pendulum import datetime

from include.utils import get_adoption_data


@dag(
    start_date=datetime(2024, 8, 1),
    schedule=None,
    catchup=False,
    doc_md=__doc__,
    tags=["2-10", "lineage"],
)
def hook_lineage_example_dag():

    @task 
    def my_python_task():
        print("Hello World")

    my_python_task()

    @task
    def get_data_from_api_1():

        data = get_adoption_data(center="center1")

        return data

    @task
    def get_data_from_api_2():

        data = get_adoption_data(center="center2")

        return data

    create_table_center_1 = SnowflakeOperator(
        task_id="create_table_center_1",
        sql="""CREATE TABLE IF NOT EXISTS adoption_center_1 (
            date DATE, type VARCHAR, name VARCHAR, age INTEGER
        );""",
    )

    create_table_center_2 = SnowflakeOperator(
        task_id="create_table_center_2",
        sql="""CREATE TABLE IF NOT EXISTS adoption_center_2 (
            date DATE, type VARCHAR, name VARCHAR, age INTEGER
        );""",
    )

    create_combo_table = SnowflakeOperator(
        task_id="create_combo_table",
        sql="""
            CREATE TABLE IF NOT EXISTS animal_adoptions_combined (
                date DATE,
                type VARCHAR,
                name VARCHAR,
                age INTEGER
                );
        """,
    )

    @task
    def insert_data(data):
        import json

        hook = SnowflakeHook("snowflake_default")

        data = json.loads(data)

        sql_values = ", ".join(
            f"('{record['date']}', '{record['type']}', '{record['name']}', {record['age']})"
            for record in data
        )

        sql_query = f"""
        INSERT INTO
            adoption_center_2 (date, type, name, age)
        VALUES
            {sql_values};
        """

        hook.run(sql_query)

    @task
    def combo_statment():
        hook = SnowflakeHook("snowflake_default")

        hook.run(
            sql="""
            INSERT INTO animal_adoptions_combined (date, type, name, age) 
                SELECT * 
                FROM adoption_center_1
                UNION 
                SELECT *
                FROM adoption_center_2;
            """,
        )

    data_1 = insert_data.override(task_id="insert_data_center_1")(
        data=get_data_from_api_1()
    )

    data_2 = insert_data.override(task_id="insert_data_center_2")(
        data=get_data_from_api_2()
    )

    combo = combo_statment()

    create_table_center_1 >> data_1 >> create_combo_table >> combo
    create_table_center_2 >> data_2 >> create_combo_table >> combo


hook_lineage_example_dag()
