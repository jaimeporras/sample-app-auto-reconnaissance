import argparse
import logging
import yaml
from asyncio import run
from services.arbiter import Arbiter

def validate_config(cfg):
    if "lattice-ip" not in cfg:
        raise ValueError("missing lattice-ip")
    if "lattice-bearer-token" not in cfg:
        raise ValueError("missing lattice-bearer-token")
    if "entity-update-rate-seconds" not in cfg:
        raise ValueError("missing entity-update-rate-seconds")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Entity Recon System')
    parser.add_argument('--config', type=str, help='Path to the configuration file', required=True)
    return parser.parse_args()

def read_config(config_path):
    with open(config_path, 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        validate_config(cfg)
    return cfg

async def main_async(cfg):
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.info("starting entity auto recon system")
    logger.info(f"got config path {cfg}")

    # Set up the application with the config
    arbiter = Arbiter(logger, cfg["lattice-ip"], cfg["lattice-bearer-token"], cfg["entity-update-rate-seconds"])
    await arbiter.start()

def main():
    args = parse_arguments()
    cfg = read_config(args.config)
    run(main_async(cfg))


if __name__ == "__main__":
    main()