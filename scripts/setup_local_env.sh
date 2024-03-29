#!/bin/bash
set -e

DIRECTORY=$(dirname $0)

HOSTNAME=localhost
WAKEUP_SERVER_PORT=5001
WAKEUP_SERVER_URL=http://$HOSTNAME:$WAKEUP_SERVER_PORT
HOMEASSISTANT_TOKEN=
HOMEASSISTANT_URL=http://homeassistant.local:8123
HOMEASSISTANT_OFFLINE_MODE=false
ZERO_MQ_SERVER_URL=tcp://localhost:5556
DEV_MODE=false
ADD_ON_HA=false
TELEGRAM_BOT_TOKEN=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--hostname) HOSTNAME="$2"; shift ;;
        -p|--wakeup_server-port) WAKEUP_SERVER_PORT="$2"; shift ;;
        -t|--homeassistant-token) HOMEASSISTANT_TOKEN="$2"; shift ;;
        -u|--homeassistant-url) HOMEASSISTANT_URL="$2"; shift ;;
        -d|--dev-mode) DEV_MODE=true ;;
        -o|--homeassistant-offline-mode) HOMEASSISTANT_OFFLINE_MODE=true ;;
        -z|--zero-mq-server-url) ZERO_MQ_SERVER_URL="$2"; shift ;;
        -b|--telegram-bot-token) TELEGRAM_BOT_TOKEN="$2"; shift ;;
        -a|--add-on-ha) ADD_ON_HA=true ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done


if [ "$HOMEASSISTANT_OFFLINE_MODE" = true ] ; then
    echo "WARNING! Setting up local environment variables... in HA offline mode"
    HOMEASSISTANT_TOKEN=fake_token_because_offline_mode
fi

if [ "$ADD_ON_HA" = true ] ; then
    echo "WARNING! Setting up local environment variables... in HA add-on mode"
    HOMEASSISTANT_URL=http://supervisor/core
fi

if [ -z "$TELEGRAM_BOT_TOKEN" ] ; then
    echo "WARNING! Telegram bot token is not set. You will not be able to use Telegram bot."
fi

echo "Setting up local environment variables... in .env file"

echo "HOSTNAME=$HOSTNAME" > $DIRECTORY/../wakeup_server/.env
echo "PORT=$WAKEUP_SERVER_PORT" >> $DIRECTORY/../wakeup_server/.env
echo "WAKEUP_SERVER_URL=$WAKEUP_SERVER_URL" >> $DIRECTORY/../wakeup_server/.env
echo "HOMEASSISTANT_TOKEN=$HOMEASSISTANT_TOKEN" >> $DIRECTORY/../wakeup_server/.env
echo "HOMEASSISTANT_URL=$HOMEASSISTANT_URL" >> $DIRECTORY/../wakeup_server/.env
echo "HOMEASSISTANT_OFFLINE_MODE=$HOMEASSISTANT_OFFLINE_MODE" >> $DIRECTORY/../wakeup_server/.env
echo "ZERO_MQ_SERVER_URL=$ZERO_MQ_SERVER_URL" >> $DIRECTORY/../wakeup_server/.env
echo "DEV_MODE=$DEV_MODE" >> $DIRECTORY/../wakeup_server/.env
echo "TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN" >> $DIRECTORY/../wakeup_server/.env

# For Docker .env.compose
echo "HOSTNAME=0.0.0.0" > $DIRECTORY/../wakeup_server/.env.compose
echo "PORT=$WAKEUP_SERVER_PORT" >> $DIRECTORY/../wakeup_server/.env.compose
echo "WAKEUP_SERVER_URL=$WAKEUP_SERVER_URL" >> $DIRECTORY/../wakeup_server/.env.compose
echo "HOMEASSISTANT_TOKEN=$HOMEASSISTANT_TOKEN" >> $DIRECTORY/../wakeup_server/.env.compose
echo "HOMEASSISTANT_URL=$HOMEASSISTANT_URL" >> $DIRECTORY/../wakeup_server/.env.compose
echo "HOMEASSISTANT_OFFLINE_MODE=$HOMEASSISTANT_OFFLINE_MODE" >> $DIRECTORY/../wakeup_server/.env.compose
echo "ZERO_MQ_SERVER_URL=$ZERO_MQ_SERVER_URL" >> $DIRECTORY/../wakeup_server/.env.compose
echo "DEV_MODE=$DEV_MODE" >> $DIRECTORY/../wakeup_server/.env.compose
echo "TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN" >> $DIRECTORY/../wakeup_server/.env.compose


# For morse vision
echo "ID=tmp_id_1" >> $DIRECTORY/../morse_vision/env_trigger.txt
echo "ZMQ_SERVER=tcp://*:5556" >> $DIRECTORY/../morse_vision/env_trigger.txt
echo "WAKEUP_SERVER_URL=$WAKEUP_SERVER_URL" > $DIRECTORY/../morse_vision/env_trigger.txt
echo "CHANNEL=0"  >> $DIRECTORY/../morse_vision/env_trigger.txt
echo "CLOSED_EYES_FRAME=3" >> $DIRECTORY/../morse_vision/env_trigger.txt
echo "BLINKING_RATIO=4.5" >> $DIRECTORY/../morse_vision/env_trigger.txt
echo "MIN_BLINKING_TIME=0.1" >> $DIRECTORY/../morse_vision/env_trigger.txt
echo "MAX_SHORT_BLINKING_TIME=0.6" >> $DIRECTORY/../morse_vision/env_trigger.txt
echo "TIMEOUT_MORSE_READER=1.5" >> $DIRECTORY/../morse_vision/env_trigger.txt


# For morse audio
echo "WAKEUP_SERVER_URL=$WAKEUP_SERVER_URL" > $DIRECTORY/../morse_audio/env_trigger.txt
echo "ID=tmp_id" >> $DIRECTORY/../morse_audio/env_trigger.txt
echo "ZMQ_SERVER=tcp://*:5556" >> $DIRECTORY/../morse_audio/env_trigger.txt
echo "RECORD_SECONDS=10" >> $DIRECTORY/../morse_audio/env_trigger.txt
echo "THRESHOLD=1400" >> $DIRECTORY/../morse_audio/env_trigger.txt
echo "END_WORD_TIME=1" >> $DIRECTORY/../morse_audio/env_trigger.txt
echo "START_LISTEN_TIME=50" >> $DIRECTORY/../morse_audio/env_trigger.txt
echo "MAX_DASHES_FOR_DOT=20" >> $DIRECTORY/../morse_audio/env_trigger.txt
echo "MIN_DASHES_FOR_DASH=5" >> $DIRECTORY/../morse_audio/env_trigger.txt


# For fall detection (upper body)
echo "WAKEUP_SERVER_URL=$WAKEUP_SERVER_URL" > $DIRECTORY/../fall_detection/env_trigger.txt
echo "ID=tmp_id" >> $DIRECTORY/../fall_detection/env_trigger.txt
echo "ZMQ_SERVER=tcp://*:5556" >> $DIRECTORY/../fall_detection/env_trigger.txt
echo "MAX_ANGLE_BETWEEN_EYES=50" >> $DIRECTORY/../fall_detection/env_trigger.txt
echo "MAX_ANGLE_BETWEEN_EARS=50" >> $DIRECTORY/../fall_detection/env_trigger.txt
echo "MAX_ANGLE_BETWEEN_SHOULDERS=50" >> $DIRECTORY/../fall_detection/env_trigger.txt


echo "Finished setting up local environment variables."
echo "----> PORT=$WAKEUP_SERVER_PORT"
echo "----> HOMEASSISTANT_URL=$HOMEASSISTANT_URL"
echo "----> HOMEASSISTANT_OFFLINE_MODE=$HOMEASSISTANT_OFFLINE_MODE"
echo "----> ZERO_MQ_SERVER_URL=$ZERO_MQ_SERVER_URL"
echo "----> DEV_MODE=$DEV_MODE"

