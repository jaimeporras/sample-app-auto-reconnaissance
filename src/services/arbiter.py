from logging import Logger
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import time
import os

from services.entity_streamer import EntityStreamer
# cache_manager -> stores all assets (fighter, uav, tank)
# another --> stores all the non-friendly  (ontology.template.track)
from services.tasker import Tasker
from utils.distance_calculator import DistanceCalculator

class Arbiter:
    def __init__(self, logger: Logger, lattice_ip: str, bearer_token: str, update_rate_seconds: int):
        print("KEVFIX ARBITER INIT", lattice_ip, bearer_token)
        self.logger = logger
        self.update_rate_seconds = update_rate_seconds
        self.entity_streamer = EntityStreamer(logger, lattice_ip, bearer_token)

    async def start(self):
        while True:
            await self.consume_entities()
            await asyncio.sleep(self.update_rate_seconds)
        #self.entity_streamer.start()
        #self.normal_processing()
        #self.tasker.start()

    async def consume_entities(self):
        async for entity in self.entity_streamer.stream_entities():
            print("KEVFIX IN CONSUME_ENTITIES", entity)
            pass

    def normal_processing(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            lambda: asyncio.run(self.entity_streamer.stream_entities()),
            "interval",
            seconds=self.update_rate_seconds,
        )
        scheduler.start()

        self.logger.info("Press Ctrl+{0} to exit".format("Break" if os.name == "nt" else "C"))
        try:
            # This is here to simulate application activity (which keeps the main thread alive).
            while True:
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            # Not strictly necessary if daemonic mode is enabled but should be done if possible
            self.logger.info("shutting down tle-lattice-integration")
            scheduler.shutdown()