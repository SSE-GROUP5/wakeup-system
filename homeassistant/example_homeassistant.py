from constants import HOMEASSISTANT_TOKEN
from homeassistant_client import HomeAssistantClient

ha_client = HomeAssistantClient(HOMEASSISTANT_TOKEN)
smart_plug_id = ha_client.find_entity_id("outlet")
ha_client.toggle(smart_plug_id)