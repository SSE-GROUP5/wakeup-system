import pytest


def test_get_signal_for_user(client):
    pass


def test_receive_signal(client):
    pass
    
    
def test_set_signal(client):
    trigger = client.post("/interactive_devices", json={"name": "andy_vision", "type": "SOUND"})
    trigger_id = trigger.get_json()["id"]
    target = client.post("/target_devices", json={"matter_id": "switch.smart_plug_mini2", "name": "Fake Matter Device", "type": "switch"})
    target_id = target.get_json()["matter_id"]
    
    response = client.post("/signals/set", json = {
        "interactive_device_id": trigger_id,
        "interactive_device_action": "taps",
        "interactive_device_num_actions": 3, 
        "target_device_id": target_id,
        "target_action": "turn_off"
    })
   
    body = response.get_json()
    assert response.status_code == 201
    assert "Signal set" == body["message"]
    new_signal = body ["signal"]
    assert new_signal["interactive_device_id"] == trigger_id
    assert new_signal["interactive_device_action"] == "taps"
    assert new_signal["interactive_device_num_actions"] == 3
    assert new_signal["target_id"] == target_id
    assert new_signal["target_action"] == "turn_off"
    
    
def test_get_signal(client):
    test_set_signal(client)
    response = client.get("/signals")
    signal_list = response.get_json()['signals']
    assert response.status_code == 200 and len(signal_list) == 1

    return signal_list
