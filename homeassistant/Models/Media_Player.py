from Models.Base import Base

class Media_Player(Base):
    
    def __init__(self, id, homeassistant_client):
        super().__init__(id, homeassistant_client)
        
    def media_pause(self):
        self.homeassistant_client.set_state(self.id, 'media_pause')
        
    def media_play(self):
        self.homeassistant_client.set_state(self.id, 'media_play')
        
    def media_play_pause(self):
        self.homeassistant_client.set_state(self.id, 'media_play_pause')
        
    def media_previous_track(self):
        self.homeassistant_client.set_state(self.id, 'media_previous_track')
    
    def media_next_track(self):
        self.homeassistant_client.set_state(self.id, 'media_next_track')
        
    def volume_up(self):
        self.homeassistant_client.set_state(self.id, 'volume_up')
        
    def volume_down(self):
        self.homeassistant_client.set_state(self.id, 'volume_down')
        
    def volume_mute(self, mute: bool = None):
        print("WARNING: volume_mute is not implemented yet, using media_play_pause instead")
        current_state = self.homeassistant_client.get_state(self.id)
        state = current_state['state']
        
        if mute == None:
            mute = True if state == "playing" else False
        
        if state == "playing" and mute:
            self.media_pause()
        elif state == "paused" and not mute:
            self.media_play()
        else:
            print("Not doing anything, state is: " + state)
        
    def volume_set(self, volume: float):
        if volume < 0 or volume > 1:
            raise ValueError("Volume must be between 0 and 1")
      
        self.homeassistant_client.set_state(self.id, 'volume_set', { 'volume_level': volume })
      
    def media_next_track(self):
        self.homeassistant_client.set_state(self.id, 'media_next_track')
    
    def media_previous_track(self):
        self.homeassistant_client.set_state(self.id, 'media_previous_track')