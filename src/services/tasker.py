from logging import Logger
import json
from openapi_client.api_client import ApiClient, Configuration
from openapi_client.api.task_api import TaskApi
from openapi_client.models.task_creation import TaskCreation
from openapi_client.models.task import Task
from openapi_client.models.task_entity import TaskEntity
from openapi_client.models.entity import Entity


class Tasker:
    def __init__(self, logger: Logger, lattice_ip: str, bearer_token: str):
        self.logger = logger
        config = Configuration(host=lattice_ip, access_token=bearer_token)
        self.api_client = ApiClient(configuration=config)
        self.task_api = TaskApi(api_client=self.api_client)

    def send_task(self, task: TaskCreation) -> Task:
        try:
            self.task_api.create_task(task)
            return task
        except Exception as e:
            self.logger.error(f"task creation error {e}")
            raise e
        
    def create_task(self, entity: Entity) -> TaskCreation:
        try:
            pass
        except Exception as e:
            raise e