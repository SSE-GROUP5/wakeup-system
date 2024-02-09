class Base():
    def __init__(self, id, homeassistant_client):
        self.id = id
        self.homeassistant_client = homeassistant_client
        
    def json(self):
        return {
            'id': self.id,
            'state': self.get_state(),
            'possible_actions': self.get_possible_actions()
        }   
        
    def get_id(self):
        return self.id
      
    def get_state(self):
        return self.homeassistant_client.get_state(self.id)
      
    def get_possible_actions(self):
        return self.homeassistant_client.get_possible_actions(self.id)
      
