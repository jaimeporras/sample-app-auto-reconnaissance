import asyncio
from logging import Logger
import entities_api as EM
from datetime import datetime, timezone

class EntityHandler:
    def __init__(self, logger: Logger, lattice_ip: str, bearer_token: str):
        self.logger = logger
        self.config = EM.Configuration(host=f"{lattice_ip}/api/v1")
        self.api_client = EM.ApiClient(configuration=self.config, header_name="Authorization", header_value=f"Bearer {bearer_token}")
        self.entity_api = EM.EntityApi(api_client=self.api_client)


    def filter_entity(self, entity: EM.Entity) -> bool:
        """
        The statement returned basically filters for 1) an entity with the ontology.template field set to ASSET, or 2) an entity with the ontology.template field set to TRACK and their mil_view.disposition field set to HOSTILE or SUSPICIOUS.
        
        Args:
            None

        Returns:
            bool: True if the entity satisfies the filter, False otherwise.

        Raises:
            None
        """
        ontology_template = entity.ontology.template
        mil_view_disposition = entity.mil_view.disposition
        if ontology_template == "TEMPLATE_ASSET":
            return True
        elif (ontology_template == "TEMPLATE_TRACK" and
                mil_view_disposition != "DISPOSITION_FRIENDLY"):
            return True
        else:
            return False

    
    async def stream_entities(self):
        entity_event_request = EM.EntityEventRequest(sessionToken="")
        while True:
            try:
                response = self.entity_api.long_poll_entity_events(entity_event_request)
                if response.entity_events:
                    # self.logger.info(f"lattice api stream entities {response.entity_events}")
                    for entity_event in response.entity_events:
                        entity = entity_event.entity
                        if self.filter_entity(entity):
                            # self.logger.info("KEVFIX entity is either asset or non-friendly track")
                            yield entity
                await asyncio.sleep(0.1)
            except Exception as error:
                self.logger.error(f"lattice api stream entities error {error}")
                await asyncio.sleep(30)

    
    def override_track_disposition(self, track: EM.Entity):
        try:
            entity_id = track.entity_id
            override_track_entity = track
            override_track_entity.mil_view.disposition = "DISPOSITION_SUSPICIOUS"
            override_provenance = EM.Provenance(integrationName=track.provenance.integration_name,
                                                dataType=track.provenance.data_type,
                                                source=track.provenance.source,
                                                sourceId=track.provenance.source_id,
                                                sourceUpdateTime= datetime.now(timezone.utc).isoformat(),
                                                sourceDescription=track.provenance.source_description,)
            entity_override = EM.EntityOverride(entity=override_track_entity, provenance=override_provenance)
            response = self.entity_api.put_entity_override_rest(entity_id=entity_id,
                                                field_path="mil_view.disposition",
                                                entity_override=entity_override)
            self.logger.info(f"KEVFIX Override for track {track.entity_id} was successful")
            return
        except Exception as error:
            self.logger.error(f"lattice api stream entities error {error}")