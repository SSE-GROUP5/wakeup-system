import pytest


def test_receive_signal(client):
    pass
    
    
def test_set_signal(client):
    trigger = client.post("/triggers", json={"name": "andy_vision", "type": "vision_blink"})
    trigger_id = trigger.get_json()["id"]
    trigger_name = trigger.get_json()["name"]
    target = client.post("/target_devices", json={"matter_id": "switch.smart_plug_mini2", "name": "Fake Matter Device", "type": "switch"})
    target_id = target.get_json()["matter_id"]
    user = client.post("/users", json = {"first_name": "test", "last_name": "user", "gosh_id": "001"})
    user_id = user.get_json()["id"]

    user = client.post("/users", json = {"first_name": "test", "last_name": "user", "gosh_id": "001"})
    user_id = user.get_json()["id"]

    
    response = client.post("/signals/set", json = {
        "trigger_id": trigger_id,
        "trigger_name": trigger_name,
        "trigger_action": "vision_blink",
        "trigger_num_actions": 3, 
        "target_device_id": target_id,
        "target_action": "turn_off",
        "user_id": user_id
    })
    body = response.get_json()
    assert response.status_code == 201
    assert "Signal set" == body["message"]
    new_signal = body ["signal"]
    assert new_signal["trigger_id"] == trigger_id
    assert new_signal["trigger_action"] == "vision_blink"
    assert new_signal["trigger_num_actions"] == 3
    assert new_signal["target_id"] == target_id
    assert new_signal["target_action"] == "turn_off"
    
    
def test_get_signal(client):
    trigger = client.post("/triggers", json={"name": "andy_vision", "type": "vision_blink"})
    trigger_id = trigger.get_json()["id"]
    trigger_name = trigger.get_json()["name"]
    target = client.post("/target_devices", json={"matter_id": "switch.smart_plug_mini2", "name": "Fake Matter Device", "type": "switch"})
    target_id = target.get_json()["matter_id"]
    user = client.post("/users", json = {"first_name": "test", "last_name": "user", "gosh_id": "001"})
    user_id = user.get_json()["id"]

    client.post("/signals/set", json = {
        "trigger_id": trigger_id,
        "trigger_name": trigger_name,
        "trigger_action": "vision_blink",
        "trigger_num_actions": 3, 
        "target_device_id": target_id,
        "target_action": "turn_off",
        "user_id": user_id
    })

    response = client.get("/signals")
    signal_list = response.get_json()['signals']
    assert response.status_code == 200 and len(signal_list) == 1

    return signal_list


# def test_get_signal_for_user(client):
#     trigger = client.post("/triggers", json={"name": "andy_vision", "type": "vision_blink"})
#     trigger_id = trigger.get_json()["id"]
#     trigger_name = trigger.get_json()["name"]
#     target = client.post("/target_devices", json={"matter_id": "switch.smart_plug_mini2", "name": "Fake Matter Device", "type": "switch"})
#     target_id = target.get_json()["matter_id"]
#     user = client.post("/users", json = {"first_name": "test", "last_name": "user", "gosh_id": "001"})
#     user_id = user.get_json()["id"]
    
#     client.post("/signals/set", json = {
#         "trigger_id": trigger_id,
#         "trigger_name": trigger_name,
#         "trigger_action": "vision_blink",
#         "trigger_num_actions": 3, 
#         "target_device_id": target_id,
#         "target_action": "turn_off",
#         "user_id": user_id
#     })

#     response = client.get("/signals/users/"+user_id)
#     signal_list = response.get_json()['signals']
#     assert response.status_code == 200 and len(signal_list) == 1


