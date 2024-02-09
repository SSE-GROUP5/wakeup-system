from homeassistant.Models.Base import Base

class Switch(Base):
  
  def __init__(self, id, homeassistant_client):
    super().__init__(id, homeassistant_client)
    
  def turn_on(self):
    self.homeassistant_client.set_state(self.id, 'turn_on')
    
  def turn_off(self):
    self.homeassistant_client.set_state(self.id, 'turn_off')
  
  def toggle(self):
    self.homeassistant_client.set_state(self.id, 'toggle')
    
  def set_state(self, state):
    cases = {
      'turn_on': self.turn_on,
      'turn_off': self.turn_off,
      'toggle': self.toggle
    }
    
    func = cases.get(state)
    if func:
      func()
    else:
      raise Exception('Invalid state')
        