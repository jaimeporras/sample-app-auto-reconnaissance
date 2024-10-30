import time
from logging import Logger
from typing import Optional
import asyncio
"""
from anduril.entitymanager.v1 import (
    EntityManagerApiStub,
    StreamEntityComponentsRequest,
    StreamEntityComponentsResponse,
)
"""
from grpclib.client import Channel

ONTOLOGY_TEMPLATES_TO_FILTER = ["TRACK", "ASSET"]

import anduril.entitymanager.v1 as EM
import anduril.ontology.v1 as ONTOLOGY

class EntityStreamer:
    def __init__(self, logger: Logger, lattice_ip: str, bearer_token: str):
        self.logger = logger
        self.lattice_ip = lattice_ip
        self.generated_metadata = {"authorization": "Bearer " + bearer_token}

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
                field_path="entity.mil_view.disposition",
                value=ONTOLOGY.Disposition.HOSTILE,
                comparator=EM.Comparator.EQUALITY
            ),
            EM.Predicate(
                field_path="entity.mil_view.disposition",
                value=ONTOLOGY.Disposition.SUSPICIOUS,
                comparator=EM.Comparator.EQUALITY
            )
        ]
        
        statement_disposition = EM.Statement(or_=EM.OrOperation(predicate_set=EM.PredicateSet(predicates=predicates_mil_view_disposition)))

        statement_track = EM.Statement(predicate=EM.Predicate(field_path="entity.ontology.template", value=EM.EnumType(EM.Template.TRACK), comparator=EM.Comparator.EQUALITY))

        statement_track_and_disposition = EM.Statement(and_=EM.AndOperation(statement_set=EM.StatementSet(statements=[statement_track, statement_disposition])))

        statement_asset = EM.Statement(predicate=EM.Predicate(field_path="entity.ontology.template", value=EM.EnumType(EM.Template.ASSET), comparator=EM.Comparator.EQUALITY))

        root_statement = EM.Statement(and_=EM.OrOperation(statement_set=EM.StatementSet(statements=[statement_track_and_disposition, statement_asset])))

        return root_statement

    async def stream_entities(self):
        """
        Asynchronously retrieves entities with 1) the ontology.template field set to TRACK and mil_view.disposition set to HOSTILE or SUSPICIOUS, or 2) the ontology.template field set to ASSET from the Lattice API. Usable wrapper around the stream_entity_components API
        """
        # open secure channel and create service instance
        async with Channel(host=self.lattice_ip, port=443, ssl=True) as channel:
            entity_manager_stub = EM.EntityManagerApiStub(channel)
            root_statement = self.create_statement()
            try:
                async for response in entity_manager_stub.stream_entity_components(
                    EM.StreamEntityComponentsRequest(include_all_components=True, filter=#EM.Statement(predicate=EM.Predicate(field_path="ontology.template", value=EM.Value(enum_type=EM.EnumType(value=EM.Template.TRACK)), comparator=EM.Comparator(EM.Comparator.EQUALITY)))),
                    metadata=self.generated_metadata
                ):
                    self.logger.debug(f"lattice api stream entities response {response}")
                    yield response
            except Exception as error:
                self.logger.error(f"lattice api stream entities error {error}")


    def start(self):
        pass