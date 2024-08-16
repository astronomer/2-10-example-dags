"""
### DAG using ds_format_locale

Added ds_format_locale method in macros which allows localizing datetime formatting using Babel (#40746) 

ds_format('05', '%m', '%b', 'en_US')
> 'May'
ds_format('05', '%m', '%b', 'nl_BE') 
> 'mei'
ds_format('12/07/2024', '%d/%m/%Y', '%A %d %B %Y', 'en_US')
> 'Friday 12 July 2024'
ds_format('12/07/2024', '%d/%m/%Y', '%A %d %B %Y', 'nl_BE')
> 'vrijdag 12 juli 2024'
"""

from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from pendulum import datetime


@dag(
    start_date=datetime(2024, 8, 1),
    schedule=None,
    catchup=False,
    doc_md=__doc__,
    tags=["2-10", "babel"],
)
def babel_format():

    welcher_tag_ist_heute = BashOperator(
        task_id="welcher_tag_ist_heute",
        bash_command="echo {{ macros.ds_format_locale(ds, '%Y-%m-%d', \"EEEE, 'der' d. MMMM yyyy\", 'de_DE') }}",
        # example output: Freitag, der 16. August 2024
    )

babel_format()
