from entities_api import Configuration, ApiClient
from entities_api.models import Entity
from entities_api.api import EntityApi

def get_entity(lattice_hostname: str, bearer_token: str, entity_id: str) -> Entity:
   config = Configuration(host=f"https://lattice-7a83e.env.sandboxes.developer.anduril.com")
   api_client = ApiClient(configuration=config, header_name="Authorization", header_value=f"Bearer {bearer_token}")
   entity_api = EntityApi(api_client=api_client)
   response = entity_api.get_entity_by_id(entity_id=entity_id)
   return response

try:
   # Replace $YOUR_LATTICE_HOSTNAME and $YOUR_BEARER_TOKEN with your information.
   entity = get_entity("https://lattice-7a83e.env.sandboxes.developer.anduril.com", "eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NTQ5ODg4OTgsImlzcyI6ImFuZHVyaWwiLCJqdGkiOiJmNDg4ZDE4Mi00OWU0LTQyYWYtOTVhMi04NWY4YTAxNjQxZTgiLCJuYmYiOjE3NDcyMTI4ODgsInN1YiI6InVzZXIvMGZjNWNjMjEtMjc1YS00N2E0LTgyMjEtNjE4MjE3Y2M2ZDI5In0.A-Yo8lJCC_okP9_cuoKcduEE03d2eMLDadpSUjPQvHI", "06aa729d-b5ff-4447-891d-deea10d54673")
   print(entity)
except Exception as error:
   print(f"Lattice HTTP SDK GetEntity error {error}")