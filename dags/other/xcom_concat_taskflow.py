"""
### .concat() with the Task Flow API

"""

from airflow.decorators import dag, task
import time

@dag(start_date=None, schedule=None, catchup=False, tags=["2-10", "XCom .concat()", "demo"])
def xcom_concat_taskflow():

    @task
    def t1():
        return [1, 2, 3]

    t1_obj = t1()

    @task
    def t2():
        return [4, 5, 6, 7]

    t2_obj = t2()

    @task
    def map_me(input):
        print(f"Sleeping for {input} seconds!")
        time.sleep(input)
        print("Waking up!")

    map_me.expand(input=t1_obj.concat(t2_obj))


xcom_concat_taskflow()
