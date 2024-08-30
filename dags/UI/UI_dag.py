"""
### DAG to showcase other UI additions

This DAG shows log-coloring, task docs, as well as XCom as JSON displays.
"""

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
import logging 

t_log = logging.getLogger("airflow.task")

@dag(
    start_date=None,
    schedule=None,
    catchup=False,
    doc_md=__doc__,
    tags=["2-10", "UI", "demo"],
)
def UI_dag():

    @task
    def t1():
        return {"Best gummy bears": "Yellow", "Eaten": 19}

    t1()

    @task
    def log_coloring():
        t_log.info("If I say 'error' the log line turns red!")
        t_log.info("I warn you, this line turns yellow!")
        print("This is a normal print statement.")
        t_log.info("By changing the keywords in the config I can make this important line turn red!")
        print("Also works for regular but important print statements.")

        t_log.error("The log-level also affects the output, in this case turning it red.")
        t_log.warn("This log-level turns the line yellow.")
        t_log.critical("This line is not red. But can be made red by adding 'critical' to the keyword list.")


    @task 
    def log_groups():
        # 2.9 feature

        t_log.info("I'm a log that is always shown.")
        t_log.info("::group::My 😊 log group!")
        t_log.info("hi! I'm a hidden log! 😊")
        t_log.info("::endgroup::")
        t_log.info("I'm not hidden either.")


    log_coloring()
    log_groups()

    @task(doc_md="Task docs in **Markdown**!")
    def task_docs_one():
        return "Hello!"

    @task
    def task_docs_two(greeting: str = "Hi"):
        """
        Doc strings **render** as well! Very neat :)
        Args:
            greeting: str, (default: 'Hi')
        Returns:
            double_greeting: str
        """
        double_greeting = greeting * 2

        return double_greeting
    
    task_docs_one()
    task_docs_two()


    task_docs_three = BashOperator(
        task_id="task_docs_three",
        bash_command="echo Hi!",
        doc_md="More Markdown this time in _italics_"
    )


UI_dag()
