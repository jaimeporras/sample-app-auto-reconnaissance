# Auto Recon
Author: Kevin Li / Anduril Industries
Date: 2024-10-29
Version: 0.0.1

## Description

## How to run locally

#### First clone the repository

```bash
git clone https://github.com/anduril/ext-auto-recon.git ext-auto-recon
cd ext-auto-recon
```

> Optional: Initialize a virtual environment
> ```bash
> python3.9 -m venv .venv
> source .venv/bin/activate
> ```

#### Install dependencies

`openapi-generator generate -i anduril/taskmanager/v1/task_manager_openapi.pub.yaml -g python -o task_manager_py`
`openapi-generator generate -i anduril/entitymanager/v1/entity_manager_openapi.pub.yaml -g python -o entity_manager_py`

go in to the directories, change the name in the `setup.py` file to a better and more descriptive name (EntityManager, TaskManager, etc)

in each package, change the name of the `openapi_client` subdirectory to a better and more descriptive name (entity_manager, task_manager, etc)

`pip install setuptools`

transport the task manager and entity manager python package over to your project directory from where you ran the openapi-generator generate command
`pip install /path/to/managers`






*** We currently use `anduril-python` for `StreamEntityComponents` in the `EntityManagerAPI` within the gRPC SDK, when the corresponding component is added to the REST SDK, we will migrate this business logic over to utilize the REST SDK instead ***

Installation of the `anduril-python` dependency requires your SSH key be added to your keychain: 

https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account

```bash
pip install -r requirements.txt
```

#### Run the program

> Modify the configuration file in `var/config.yml`, add your Lattice Bearer Token

```bash
python3 src/main.py --config var/config.yml
```

