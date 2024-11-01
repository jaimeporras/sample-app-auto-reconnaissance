import asyncio
from logging import Logger
# from grpclib.client import Channel
#from entity_manager import EntityApi, Entity, ApiClient, Configuration
import entity_manager as EM
#from openapi_client.api.entity_api import EntityApi

class EntityStreamer:
    def __init__(self, logger: Logger, lattice_ip: str, bearer_token: str):
        self.logger = logger
        #self.lattice_ip = lattice_ip
        #self.generated_metadata = {"authorization": "Bearer " + bearer_token}
        self.config = EM.Configuration(host='https://dev.tdm.anduril.com/entitymanager/', access_token=bearer_token)
        self.api_client = EM.ApiClient(configuration=self.config)


    def create_statement(self) -> EM.Statement:
        """
        yuck - creating a statement to pass into the stream_entity_components API as a filter.
        The statement returned basically filters for 1) an entity with the ontology.template field set to ASSET, or 2) an entity with the ontology.template field set to TRACK and their mil_view.disposition field set to HOSTILE or SUSPICIOUS.
        
        Args:
            None

        Returns:
            EM.Statement: The retrieved encased, or None if an error occurred.

        Raises:
            None
        """
        predicates_mil_view_disposition = [
            EM.Predicate(
                field_path="mil_view.disposition",
                value=EM.Value(enum_type=EM.EnumType(value=ONTOLOGY.Disposition.HOSTILE)),
                comparator=EM.Comparator(EM.Comparator.EQUALITY)
            ),
            EM.Predicate(
                field_path="mil_view.disposition",
                value=EM.Value(enum_type=EM.EnumType(value=ONTOLOGY.Disposition.SUSPICIOUS)),
                comparator=EM.Comparator(EM.Comparator.EQUALITY)
            )
        ]
        
        statement_disposition = EM.Statement(or_=EM.OrOperation(predicate_set=EM.PredicateSet(predicates=predicates_mil_view_disposition)))

        statement_track = EM.Statement(predicate=EM.Predicate(field_path="ontology.template", value=EM.Value(enum_type=EM.EnumType(value=EM.Template.TRACK)), comparator=EM.Comparator(EM.Comparator.EQUALITY)))

        statement_track_and_disposition = EM.Statement(and_=EM.AndOperation(statement_set=EM.StatementSet(statements=[statement_track, statement_disposition])))

        statement_asset = EM.Statement(predicate=EM.Predicate(field_path="ontology.template", value=EM.Value(enum_type=EM.EnumType(value=EM.Template.ASSET)), comparator=EM.Comparator(EM.Comparator.EQUALITY)))

        root_statement = EM.Statement(or_=EM.OrOperation(statement_set=EM.StatementSet(statements=[statement_track_and_disposition, statement_asset])))

        return root_statement

    
    async def stream_entities(self):
        entity_api = EM.EntityApi(api_client=self.api_client)
        entity_event_request = EM.EntityEventRequest(sessionToken="")
        while True:
            try:

                response = entity_api.long_poll_entity_events(entity_event_request)
                if response.entity_events:
                    self.logger.info(f"lattice api stream entities {response.entity_events}")
                    for event in response.entity_events:
                        yield event
                await asyncio.sleep(1)
            except Exception as error:
                self.logger.error(f"lattice api stream entities error {error}")
                await asyncio.sleep(60)

    
    #async def stream_entities(self):
        """
        Asynchronously retrieves entities with 1) the ontology.template field set to TRACK and mil_view.disposition set to HOSTILE or SUSPICIOUS, or 2) the ontology.template field set to ASSET from the Lattice API. Usable wrapper around the stream_entity_components API
        """
        # open secure channel and create service instance
        """
        async with Channel(host=self.lattice_ip, port=443, ssl=True) as channel:
            entity_manager_stub = EM.EntityManagerApiStub(channel)
            root_statement = self.create_statement()
            try:
                async for response in entity_manager_stub.stream_entity_components(
                    EM.StreamEntityComponentsRequest(include_all_components=True, filter=root_statement, rate_limit=EM.RateLimit(update_per_entity_limit_ms=1000)),
                    metadata=self.generated_metadata
                ):
                    yield response
            except Exception as error:
                self.logger.error(f"lattice api stream entities error {error}")
        """