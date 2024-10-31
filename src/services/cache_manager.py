from utils.lru_cache import LRUCache
import anduril.entitymanager.v1 as EM
import anduril.ontology.v1 as ONTOLOGY

class CacheManager:
    def __init__(self, capacity: int = 100):
        self.assets = LRUCache(capacity)
        self.tracks = LRUCache(capacity)


    def add_asset(self, entity: EM.Entity):
        entity_id = entity.entity_id
        self.assets.put(entity_id, entity)

    def add_track(self, entity: EM.Entity):
        entity_id = entity.entity_id
        self.tracks.put(entity_id, entity)
        
    def get_assets(self) -> list[EM.Entity]:
        return self.assets.get_all()

    def get_tracks(self) -> list[EM.Entity]:
        return self.tracks.get_all()
    
    def handle_response(self, response: EM.StreamEntityComponentsResponse):
        ontology_template = response.entity_event.entity.ontology.template
        mil_view_disposition = response.entity_event.entity.mil_view.disposition
        if ontology_template == EM.Template.ASSET:
            self.add_asset(response.entity_event.entity)
        elif (ontology_template == EM.Template.TRACK and
                mil_view_disposition in [ONTOLOGY.Disposition.HOSTILE, ONTOLOGY.Disposition.SUSPICIOUS]):
            self.add_track(response.entity_event.entity)