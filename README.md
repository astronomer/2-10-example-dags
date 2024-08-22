# Apache Airflow 2.10 example DAGs

This repository contains example DAGs showing features released in Apache Airflow 2.9. 

Aside from core Apache Airflow this project uses:
- The [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) to run Airflow locally (version 1.28.1).
- The [Snowflake Airflow provider](https://registry.astronomer.io/providers/apache-airflow-providers-snowflake/versions/latest).
- The [Open Lineage Airflow provider](https://airflow.apache.org/docs/apache-airflow-providers-openlineage/stable/index.html)

For pinned versions of the provider packages see the `requirements.txt` file.

# How to use this repository

This section explains how to run this repository with Airflow. 

> [!NOTE]  
> The `lineage_example_dag` DAG in this repository requires additional connections and tools. 
> You can define the Snowflake and AWS connection in the Airflow UI under **Admin > Connections** or by using the `.env` file with the format shown in `.env.example`.
> To set up Marquez for the [`dags/hook_lineage/lineage_example_dag.py](dags/hook_lineage/lineage_example_dag.py) DAG, follow this [tutorial](https://www.astronomer.io/docs/learn/marquez).
> Open Lineage provider support for hook-level lineage will be added to an upcoming provider release, see https://github.com/apache/airflow/pull/41482.

See the [Manage Connections in Apache Airflow](https://docs.astronomer.io/learn/connections) guide for further instructions on Airflow connections. 

## Steps to run this repository

Download the [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) to run Airflow locally in Docker. `astro` is the only package you will need to install.

1. Run `git clone https://github.com/astronomer/2-10-example-dags.git` on your computer to create a local clone of this repository.
2. Install the Astro CLI by following the steps in the [Astro CLI documentation](https://docs.astronomer.io/astro/cli/install-cli). Docker Desktop/Docker Engine is a prerequisite, but you don't need in-depth Docker knowledge to run Airflow with the Astro CLI.
3. Run `astro dev start` in your cloned repository.
4. After your Astro project has started. View the Airflow UI at `localhost:8080`.

Most DAGs are ready to run and explore, their DAG Docs / docstrings explain what features they highlight and you can sort for DAGs centering around a related feature by using their tags.

## Useful links

- [Datasets guide](https://docs.astronomer.io/learn/airflow-datasets).
- [Dynamic Task Mapping guide](https://docs.astronomer.io/learn/dynamic-tasks).
- [Airflow and OpenLineage guide](https://www.astronomer.io/docs/learn/airflow-openlineage/).
- [Airflow + Marquez tutorial](https://www.astronomer.io/docs/learn/marquez).
- [Airflow Config reference](https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html).

# Project Structure

This repository contains the following files and folders:

- `.astro`: files necessary for Astro CLI commands.
-  `dags`: all DAGs in your Airflow environment. Files in this folder will be parsed by the Airflow scheduler when looking for DAGs to add to your environment.
- `include`: supporting files that will be included in the Airflow environment.
- `plugins`: folder to place Airflow plugins. Contains a listener plugin.
- `src`: image file for this Readme.
- `tests`: folder to place pytests running on DAGs in the Airflow instance. Contains default tests.
- `.astro-registry.yaml`: file to configure DAGs being uploaded to the [Astronomer registry](https://registry.astronomer.io/). Can be ignored for local development.
- `.dockerignore`: list of files to ignore for Docker.
- `.env.example`: example environment variables for the DAGs in this repository. Copy this file to `.env` and replace the values with your own credentials.
- `.gitignore`: list of files to ignore for git.
- `Dockerfile`: the Dockerfile using the Astro CLI. Sets environment variables to change Airflow webserver settings.
- `packages.txt`: system-level packages to be installed in the Airflow environment upon building of the Docker image. Empty.
- `README.md`: this Readme.
- `requirements.txt`: python packages to be installed to be used by DAGs upon building of the Docker image.

## Appendix

After all the DAGs in the [`dags/datasets/dataset_alias`](dags/datasets/dataset_alias) folder are run, the following dependency situation is created:

![Screenshot of a slide showing the Datasets view for the DAGs in this folder: 1. upstream_produce_to_alias_A updates my_alias with x-dataset-A -> downstream_on_alias + downstream_on_dataset_a runs. 2. upstream_produce_to_alias_B updates my_alias with x-dataset-B -> downstream_on_alias runs. 3. upstream_produce_dataset_A updates x-dataset-A  -> downstream_on_alias + downstream_on_dataset_a runs (x-dataset-A is now associated with my_alias).](src/datasetalias_overview.png)