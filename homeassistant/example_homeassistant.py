from constants import HOMEASSISTANT_TOKEN
from homeassistant_client import HomeAssistantClient


ha_client = HomeAssistantClient(HOMEASSISTANT_TOKEN)
switches = ha_client.find_switches()
media_players = ha_client.find_media_players()

switche_1 = switches[0]
switche_1.turn_on()

