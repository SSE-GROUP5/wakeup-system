# API Documentation for the WakeUp server

The WakeUp server is a server that listens to triggers and sends signals to targets. The triggers can be sound classification, sound whisper, sound morse, vision morse, vision blink, vision upper body fall. The targets can be Home Assistant devices, Telegram bot, Wake on LAN devices. 

## Start the server

If the wakeup server is not setup, you can follow the instructions [here](#setup-the-wake-up-server). 

To start the server, you can run the following command:

```bash 
  source venv/bin/activate
  python run.py
```

Test the server by running the following command:

```bash 
  curl http://localhost:5001/health
```

## View the API documentation
You can view the API documentation by going to `http://<hostname>:5001/docs`.




# Setup the wake up server

## Run the setup environement script to install all environment variables

```bash Unix
  cd .. &&
  ./scripts/setup_local_env.sh \
    -h <ip_address_of_flask_server> \
    --homeassistant-token <homeassistant_token> \
    --telegram-bot-token <telegram_bot_token> 
```

Note: Other options are available, run `./scripts/setup_local_env.sh -h`. Look at line 19 in the script for more information.


## Running the server locally

### Create a python 3.9 virtual environment and install the requirements

```bash Unix
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run the server

```bash Unix
python3 run.py
```

## Running with a docker container
We assume that you have docker installed on your machine. If not, please follow the instructions [here](https://docs.docker.com/get-docker/).

### Build and run a docker image

```bash 
  docker compose build
```

```bash 
  docker compose up -d 
```

Your server should be running on `http://localhost:5001/`.
You can test it by running the following command:

```bash 
  curl http://localhost:5001/health
```

# Setup the triggers, targets and signals
A postman collection is available in the `postman` folder. You can import it in your postman application and use it to setup the triggers, targets and signals.


## Setup a trigger

### Add a trigger

```json
{
    "type": <'sound_classification', 'sound_whisper', 'sound_morse', 'vision_morse', 'vision_blink', 'vision_upper_body_fall'>,
    "name": <choose_a_trigger_name>
}
```

```bash
curl -X POST http://<hostname>:5001/triggers -H "Content-Type: application/json" -d '{"type": "sound_classification", "name": "sound_classification_trigger"}'
```

You can also add the trigger with the postman collection.


### Save the trigger id in the environment variables of the trigger
It will return a trigger id that you need to put in the environment variables of the trigger.

```env_trigger.txt
WAKEUP_SERVER_URL=http://<hostname>:5001
ID=<id-received-from-the-previous-request>
ZMQ_SERVER=tcp://127.0.0.1:5556
```

### Confirm 

You can manually confirm the trigger by running the following command:

```bash
curl -X POST http://<hostname>:5001/triggers/confirm -H "Content-Type: application/json" -d '{"id": <id-received-from-the-previous-request>}'
```

You can also confirm the trigger with the postman collection.

## Setup a target 

### With a Home Assistant target (Matter device, spotify player, chromecast, etc.)

1. Make sure you have a Home Assistant server running, have the home assistant token and its url. 

To get the token, go to your Home Assistant OS, click on your profile, then on the bottom of the page, you will see the Long-Lived Access Tokens. Click on the `Create token` button and copy the token.

1. Make sure that the environment variables are set in the .env file of the wakeup_server. You can also re-run the setup_local_env.sh script to add the token by adding the `--homeassistant-token`, `--homeassistant-url` options.
2. You can check if the server is running by running the following command:

```bash
curl http://<hostname>:5001/health
```

The response should be `{"DEV_MODE": false, "HA_status": "ALIVE", ...}`

4. Before adding the target in the wakeup system, you need to add it in the Home Assistant OS. You can start the Matter server add-on in the Home Assistant OS by following the instructions [here](https://www.home-assistant.io/integrations/matter/#adding-a-matter-device-to-home-assistant).

5. Once the device is added in the Home Assistant OS, you can add the target in the wakeup_server by running the following command:

```bash
curl -X POST http://<hostname>:5001/target_devices -H "Content-Type: application/json" -d '{"id": "<device_id>", "name": "<device_id>", "type": "homeassistant"}'
```
The <device_id> is the id of the device in the Home Assistant OS. You can find it in the Home Assistant OS by going to the `Configuration` tab, then `Devices and services`. Open the `Device` tab and copy the id of the device you want to register. Following images show how to get the device id of a Matter smart plug. The id should look like this: `switch.smart_plug_mini` or `media_player.name_of_the_device`.

![Step_1](images/setup_matter_device_1.png)

![Step_2](images/setup_matter_device_2.png)

![Step_3](images/setup_matter_device_3.png)

You can also add the target with the postman collection.

### With a Telegram target

1. Create a telegram bot with the help of the [BotFather](https://telegram.me/BotFather)
   a. Create a new bot by sending the `/newbot` command
   b. Name your bot
   c. Copy the token and save it in the environment variables in the .env file of the wakeup_server. You can also re-run the setup_local_env.sh script to add the token by adding the `--telegram-bot-token` option.

2. Start the telegram bot by running the following command:

```bash
  python telegram_bot/telegram_bot.py 
```

3. Get the channel id 
    a. Start a chat with the bot
    b. send /id to the bot to get the chat id and copy past the id. It should look like this: telegram.1234567890


4. Add the target in the wakeup_server by running the following command:

```bash
curl -X POST http://<hostname>:5001/target_devices -H "Content-Type: application/json" -d '{"id": "<chat_id>", "name": "<chat_id>", "type": "telegram"}'
```

You can also add the target with the postman collection.


### With a Wake ON LAN target

1. Get the MAC and IP address of the device you want to wake up.
2. Add the target in the wakeup_server by running the following command:

```bash
curl -X POST http://<hostname>:5001/target_devices -H "Content-Type: application/json" -d '{"mac": "<mac_address>", "name": "<device_name>", "type": "wake_on_lan", "ip": "<ip_address>", "id": "<device_name>"}'
```

You can also add the target with the postman collection.


## Setup a signal
Now that you have a trigger and a target, you can create a signal that will link the trigger to the target. The example below shows how to create a signal that will send a message to a smart plug when you blink your eyes 3 times.

### Add a signal

```json
{
    "trigger_id": "f990fa0a-9cd5-43f7-ad36-ccc04e4ca269",
    "trigger_action": "vision_blink",
    "trigger_num_actions": 2,
    "target_device_id": "switch.smart_plug_mini_2",
    "target_action": "toggle"
}
```

```bash
curl -X POST http://<hostname>:5001/signals -H "Content-Type: application/json" -d '{"trigger_id": "<trigger_id>", "trigger_action": "vision_blink", "trigger_num_actions": 2, "target_device_id": "<target_device_id>", "target_action": "toggle"}'
```

You can also add the signal with the postman collection.

You can test the signal by running the following command:

```json
{
    "id": "f990fa0a-9cd5-43f7-ad36-ccc04e4ca269",
    "action": "vision_blink",
    "num_actions": 2
}
```

```bash
curl -X POST http://<hostname>:5001/signals -H "Content-Type: application/json" -d '{"id": "<trigger_id>", "action": "vision_blink", "num_actions": 2}'
```


# Insert the WakeUp server in the home assistant OS to run it as an add-on
The wakeup server can be inserted in the Home Assistant OS as an add-on. To do so, you need to build the docker image and insert it in the Home Assistant OS with the help of Samba share.

## Install Samba share in the Home Assistant OS

1. Go to the Home Assistant OS
2. Click on Settings
3. Click on Add-on 
4. Click on Add-on store
5. Search for Samba share and install it
6. Insert a password and click on Start

## Connect to the Samba share from your computer

### On Mac

1. Open Finder
2. Click on cmd + k
3. Enter `smb://<ip_address_of_home_assistant_os>` and click on connect
4. Enter the username and password (default username is `homeassistant` and the password is the one you entered when you installed the Samba share add-on)
5. Select the `addons` folder


### On Windows
1. Open File Explorer
2. Click on the address bar
3. Enter `\\<ip_address_of_home_assistant_os>` and click on enter
4. Enter the username and password (default username is `homeassistant` and the password is the one you entered when you installed the Samba share add-on)
5. Select the `addons` folder

## Insert the docker image in the Home Assistant OS

1. Create a folder in the `addons` folder of the Samba share and name it `wakeup_server`
2. Copy the content of the `wakeup_server` folder in the `wakeup_server` folder you just created in the `addons` folder of the Samba share. The minimum content should be in the `wakeup_server` folder:
```bash
.
├── Dockerfile
├── blueprints
├── config.yaml
├── constants.py
├── db.py
├── homeassistant
├── homeassistant_client.py
├── log_scheduler.py
├── models
├── requirements.txt
├── run.py
├── scheduler
├── static
├── wake_on_lan
├── zeromq # taken from the zeromq folder at the root of the project
└── zmq_client.py
```

Warning: Copying the whole `wakeup_server` folder will take too much space in the Home Assistant OS. You can copy only the necessary files and folders.

3. Configure the `config.yaml` file with the environment variables. The `config.yaml` file should look like in the config.yaml file in the `wakeup_server` folder.

4. Refresh the Add-on store in the Home Assistant OS

5. You should see the `wakeup_server` add-on in the Add-on store. Click on it and install it.

6. Start the add-on

7. You can access the logs of the add-on by clicking on the `Logs` tab in the add-on page. You should see the following logs:

```
TELEGRAM_BOT_TOKEN is set
HOMEASSISTANT_URL: http://supervisor/core
DEV_MODE: False
HOMEASSISTANT_OFFLINE_MODE is False
Swagger UI available at http://0.0.0.0:5001/docs
 * Serving Flask app 'run'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5001
 * Running on http://172.30.33.0:5001
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 225-891-918
192.168.1.34 - - [29/Mar/2024 18:48:52] "GET /health HTTP/1.1" 200 -
192.168.1.34 - - [29/Mar/2024 18:48:52] "GET /favicon.ico HTTP/1.1" 404 -
192.168.1.34 - - [29/Mar/2024 18:50:09] "GET / HTTP/1.1" 200 -
```

8. You can access the wakeup server by going to `http://<home_assistant_url>:5001/heath` and its swagger documentation by going to `http://<home_assistant_url>:5001/docs`



# Test the wakeup server
The WakeUp server can be tested with pytest. To run the tests, you need to install the requirements in the `requirements-dev.txt` file and run the following command from the wakeup_server folder:

```bash
pytest
```

The pytest tests are also run in the Github actions. You can see the results in the `Actions` tab of the Github repository.