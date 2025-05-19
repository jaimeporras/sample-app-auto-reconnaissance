import argparse
import asyncio
import logging
from datetime import datetime, timezone, timedelta

import entities_api as anduril_entities
import yaml

EXPIRY_OFFSET = 15
REFRESH_INTERVAL = 5


class SimulatedTrack:
    def __init__(self,
                 logger: logging.Logger,
                 entities_api_client: anduril_entities.EntityApi,
                 entity_id: str,
                 location: dict):
        self.logger = logger
        self.entities_api_client = entities_api_client
        self.entity_id = entity_id
        self.location = location

    async def run(self):
        self.logger.info(f"starting publish task for simulated track {self.entity_id}")
        while True:
            try:
                self.entities_api_client.publish_entity_rest(
                    entity=self.generate_track_entity()
                )
                self.logger.info(f"published track entity {self.entity_id}")
            except Exception as error:
                self.logger.error(f"lattice api stream track error {error}")
            await asyncio.sleep(REFRESH_INTERVAL)

    def generate_track_entity(self):
        return anduril_entities.Entity(
            entity_id=self.entity_id,
            is_live=True,
            expiry_time=datetime.now(timezone.utc) + timedelta(seconds=EXPIRY_OFFSET),
            aliases=anduril_entities.Aliases(
                name=f"Simulated Track {self.entity_id}",
            ),
            location=anduril_entities.Location(
                position=anduril_entities.Position(
                    latitudeDegrees=self.location["latitude"],
                    longitudeDegrees=self.location["longitude"],
                    altitudeHaeMeters=0
                ),
                speedMps=1,
                velocityEnu=anduril_entities.ENU(
                    e=1,
                    n=1,
                    u=0
                )
            ),
            mil_view=anduril_entities.MilView(
                disposition="DISPOSITION_UNKNOWN",
                environment="ENVIRONMENT_SURFACE",
            ),
            provenance=anduril_entities.Provenance(
                data_type="Simulated Track",
                integration_name="auto-reconnaissance-sample-app",
                source_update_time=datetime.now(timezone.utc),
            ),
            ontology=anduril_entities.Ontology(
                template="TEMPLATE_TRACK",
                platform_type="UNKNOWN"
            )
        )


def validate_config(cfg):
    if "lattice-ip" not in cfg:
        raise ValueError("missing lattice-ip")
    if "lattice-bearer-token" not in cfg:
        raise ValueError("missing lattice-bearer-token")
    if "sandbox-token" not in cfg:
        raise ValueError("missing sandbox-token")
    if "latitude" not in cfg:
        raise ValueError("missing latitude")
    if "longitude" not in cfg:
        raise ValueError("missing longitude")


def parse_arguments():
    parser = argparse.ArgumentParser(description='Simulated Track')
    parser.add_argument('--config', type=str, help='Path to the configuration file', required=True)
    return parser.parse_args()


def read_config(config_path):
    with open(config_path, 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        validate_config(cfg)
    return cfg


def main():
    logging.basicConfig()
    logger = logging.getLogger("SIMTRACK")
    logger.setLevel(logging.DEBUG)
    logger.info("starting simulated track")

    args = parse_arguments()
    cfg = read_config(args.config)

    entities_configuration = anduril_entities.Configuration(
        host=f"https://{cfg['lattice-ip']}/api/v1"
    )
    entities_api_client = anduril_entities.ApiClient(configuration=entities_configuration)
    entities_api_client.default_headers["Authorization"] = f"Bearer {cfg['lattice-bearer-token']}"
    entities_api_client.default_headers["anduril-sandbox-authorization"] = f"Bearer {cfg['sandbox-token']}"
    entities_api = anduril_entities.EntityApi(api_client=entities_api_client)

    track = SimulatedTrack(
        logger,
        entities_api,
        "track-01",
        {"latitude": cfg["latitude"], "longitude": cfg["longitude"]}
    )

    try:
        asyncio.run(track.run())
    except KeyboardInterrupt:
        logger.info("keyboard interrupt detected")


if __name__ == "__main__":
    main()
