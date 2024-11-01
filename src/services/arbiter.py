import asyncio
from logging import Logger
from services.entity_streamer import EntityStreamer
from services.cache_manager import CacheManager
from services.tasker import Tasker
from utils.distance_calculator import DistanceCalculator

class Arbiter:
    def __init__(self, logger: Logger, lattice_ip: str, bearer_token: str, update_rate_seconds: int):
        self.logger = logger
        self.entity_streamer = EntityStreamer(logger, lattice_ip, bearer_token)
        self.cache_manager = CacheManager()
        self.tasker = Tasker(logger, lattice_ip, bearer_token)
 
    async def start(self):
        try:
            asyncio.create_task(self.consume_entities())
            asyncio.create_task(self.recon_job())
            await asyncio.Event().wait()
        except (KeyboardInterrupt, SystemExit):
            self.logger.info("shutting down Entity Auto Recon System")

    async def consume_entities(self):
        while True:
            async for entity_event in self.entity_streamer.stream_entities():
                self.logger.info(f"KEVFIX STREAM RESPONSE {entity_event}")
                self.cache_manager.handle_response(entity_event)
    
    async def recon_job(self):
        while True:
            self.logger.info("KEVFIX RECON JOB")
            self.calculate_within_range()
            await asyncio.sleep(1)

    def calculate_within_range(self):
        assets = self.cache_manager.get_assets()
        tracks = self.cache_manager.get_tracks()
        self.logger.info(f"KEVFIX ASSET SIZE {len(assets)} TRACK SIZE {len(tracks)}")
        for asset in assets:
            for track in tracks:
                distance = DistanceCalculator.calculate(asset, track)
                if distance <= 30000:
                    self.logger.info(f"KEVFIX DISTANCE {distance}")
                    self.tasker.create_task(asset.to_json())
                    #self.tasker.investigate(asset, track)