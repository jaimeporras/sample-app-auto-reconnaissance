from logging import Logger
import tasks_api as TM
import entities_api as EM


class Tasker:
    def __init__(self, logger: Logger, lattice_ip: str, bearer_token: str):
        self.logger = logger
        self.config = TM.Configuration(host=f"{lattice_ip}/api/v1")
        self.api_client = TM.ApiClient(configuration=self.config, header_name="Authorization", header_value=f"Bearer {bearer_token}")
        self.task_api = TM.TaskApi(api_client=self.api_client)
        #self.logger.info(f"KEVFIX MODELS {dir(openapi_client.models)}")
        
    def investigate(self, asset: EM.Entity, track: EM.Entity) -> str:
        try:
            # we have to convert EM.Entity to TM.Entity to be able to use these instances for task creation
            tm_asset = TM.Entity(**asset.to_dict())
            tm_track = TM.Entity(**track.to_dict())

            display_name = f"Asset {tm_asset.entity_id} -> Track {tm_track.entity_id}"
            description = f"Asset {tm_asset.entity_id} tasked to perform ISR on Track {tm_track.entity_id}"
            specification_type = "type.googleapis.com/anduril.tasks.v2.Investigate"
            specification_properties = {
                "objective": {
                    "entity_id": tm_track.entity_id
                },
                "parameters": {
                    "speed_m_s": tm_asset.location.speed_mps
                }
            }
            specification = TM.GoogleProtobufAny(type=specification_type,
                                                 additional_properties=specification_properties)
            author_user = TM.User(userId="user/de09bc8a-dc2b-47d7-bf7b-afa29d48be8a")
            author = TM.Principal(user=author_user)
            relations_assignee_system = TM.System(entityId=tm_asset.entity_id,
                                                  assetId=tm_asset.aliases.alternate_ids[0].id)
            relations_assignee = TM.Principal(system=relations_assignee_system)
            relations = TM.Relations(assignee=relations_assignee)
            self.logger.info(f"KEVFIX entity_asset type {type(tm_asset) } \n KEVFIX asset type {type(asset)}")
            task_entity = TM.TaskEntity(entity=tm_asset, snapshot=False)

            task_creation = TM.TaskCreation(displayName=display_name,
                                            description=description,
                                            specification=specification,
                                            author=author,
                                            relations=relations,
                                            isExecutedElsewhere=False,
                                            initialEntities=[task_entity])
            self.logger.info(f"KEVFIX {task_creation.to_str()}")
            returned_task = self.task_api.create_task(task_creation=task_creation,
                                                      _content_type="application/json")
            self.logger.info(f"KEVFIX task created - view Lattice UI, task id is {returned_task.version.task_id}")
            return returned_task.version.task_id
        except Exception as e:
            self.logger.error(f"task creation error {e}")
            raise e
        
    def check_availability(self, task_id: str) -> str:
        try:
            returned_task = self.task_api.get_task_by_id(taskId=task_id)
            return returned_task
        except Exception as e:
            self.logger.error(f"task creation error {e}")
            raise e