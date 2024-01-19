class Base():
    def __init__(self, id, homeassistant_client):
        self.id = id
        self.homeassistant_client = homeassistant_client
        
    def get_id(self):
        return self.id
      
    def get_state(self):
        return self.homeassistant_client.get_state(self.id)
      
    def get_possible_actions(self):
        return self.homeassistant_client.get_possible_actions(self.id)
      
