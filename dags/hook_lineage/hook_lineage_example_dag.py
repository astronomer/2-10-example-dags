"""
### Lineage Example DAG

NOTE: OpenLineage provider support for Hook lineage is incoming in the next release.
See https://github.com/apache/airflow/pull/41482 for more information.
"""

from airflow.decorators import dag, task
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from pendulum import datetime

from include.utils import get_adoption_data

import os

_MY_BUCKET = os.getenv("MY_BUCKET", "my-bucket")


@dag(
    start_date=datetime(2024, 8, 1),
    schedule=None,
    catchup=False,
    doc_md=__doc__,
    tags=["2-10", "lineage"],
)
def lineage_example_dag():

    # --------------------------- #
    # Basic Lineage Example using #
    # --------------------------- #

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

    # -------------------------------------- #
    # S3 Hook example for added Hook Lineage #
    # -------------------------------------- #

    @task
    def s3_1():
        import io

        hook = S3Hook(aws_conn_id="aws_default")

        file_obj = io.BytesIO(b"Hello, World!")

        hook.load_file_obj(
            file_obj=file_obj,
            key="my_file6.txt",
            bucket_name=_MY_BUCKET,
        )

    @task
    def s3_2():
        import io

        hook = S3Hook(aws_conn_id="aws_default")

        file_obj = hook.read_key(key="my_file6.txt", bucket_name=_MY_BUCKET)

        return file_obj

    s3_1() >> s3_2()


lineage_example_dag()
