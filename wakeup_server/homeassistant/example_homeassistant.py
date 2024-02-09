from constants import HOMEASSISTANT_TOKEN
from homeassistant_client import HomeAssistantClient


ha_client = HomeAssistantClient(HOMEASSISTANT_TOKEN)
devices = ha_client.find_entity_by_attributes()
print(devices)