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
    logger = logging.getLogger("EARS")
    logger.setLevel(logging.DEBUG)
    logger.info("starting Entity Auto Recon System")
    try:
        # Set up the application with the config
        arbiter = Arbiter(logger, cfg["lattice-ip"], cfg["lattice-bearer-token"])
        await arbiter.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("shutting down Entity Auto Recon System")

def main():
    args = parse_arguments()
    cfg = read_config(args.config)
    try:
        run(main_async(cfg))
    except KeyboardInterrupt:
        print("shutting down Entity Auto Recon System")


if __name__ == "__main__":
    main()