import argparse
import asyncio
import logging
from asyncio import run
from datetime import datetime, timezone
from logging import Logger

import entities_api
import entities_api as anduril_entities
import yaml


class SimulatedAsset:
    def __init__(self, logger: Logger, entities_api_client: anduril_entities.EntityApi, entity_id: str,
                 location: dict):
        self.logger = logger
        self.entities_api_client = entities_api_client
        self.entity_id = entity_id
        self.location = location

    async def run(self):
        tasks = [
            asyncio.create_task(self.publish_asset()),
            asyncio.create_task(self.listen_for_tasks())
        ]
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except KeyboardInterrupt:
            self.logger.info("KeyboardInterrupt caught: cancelling tasks...")
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
        finally:
            self.logger.info("Shutting down Simulated Asset {}".format(self.entity_id))
        pass

    async def publish_asset(self):
        while True:
            self.entities_api_client.publish_entity_rest(
                entity=self.generate_asset_entity()
            )
            await asyncio.sleep(1)

    async def listen_for_tasks(self):
        pass

    def generate_asset_entity(self):
        return entities_api.Entity(
            entity_id=self.entity_id,
            is_live=True,
            location=entities_api.Location(
                position=entities_api.Position(
                    latitude_degrees=self.location["latitude"],
                    longitude_degrees=self.location["longitude"]
                )
            ),
            mil_view=entities_api.MilView(
                disposition="DISPOSITION_FRIENDLY",
                environment="ENVIRONMENT_SURFACE",
            ),
            provenance=entities_api.Provenance(
                data_type="DDG",
                integration_name="Simulated Asset",
                source_update_time=datetime.now(timezone.utc),
            )
        )
        pass


def validate_config(cfg):
    if "lattice-ip" not in cfg:
        raise ValueError("missing lattice-ip")
    if "lattice-bearer-token" not in cfg:
        raise ValueError("missing lattice-bearer-token")


def parse_arguments():
    parser = argparse.ArgumentParser(description='Simulated Asset')
    parser.add_argument('--config', type=str, help='Path to the configuration file', required=True)
    return parser.parse_args()


def read_config(config_path):
    with open(config_path, 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        validate_config(cfg)
    return cfg


def main():
    logging.basicConfig()
    logger = logging.getLogger("SIMASSET")
    logger.setLevel(logging.DEBUG)
    logger.info("starting simulated asset")

    args = parse_arguments()
    cfg = read_config(args.config)
    entities_configuration = anduril_entities.Configuration(host=f"{cfg['lattice-ip']}/api/v1")
    entities_api_client = anduril_entities.ApiClient(configuration=entities_configuration,
                                                     header_name="Authorization",
                                                     header_value=f"Bearer {cfg['lattice-bearer-token']}")
    entities_api = anduril_entities.EntityApi(api_client=entities_api_client)

    asset = SimulatedAsset(
        logger,
        entities_api,
        "asset-01",
        {"latitude": 1, "longitude": 1})

    try:
        run(asset.run())
    except KeyboardInterrupt:
        print("shutting down simulated asset")
    pass
