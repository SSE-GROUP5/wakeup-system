#!/bin/bash
set -e

DIRECTORY=$(dirname $0)

HOSTNAME=localhost
WAKEUP_SERVER_PORT=5001
HOMEASSISTANT_TOKEN=
HOMEASSISTANT_URL=http://homeassistant.local:8123
HOMEASSISTANT_OFFLINE_MODE=false
ZERO_MQ_SERVER_URL=tcp://localhost:5556
DEV_MODE=false
ADD_ON_HA=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -h|--hostname) HOSTNAME="$2"; shift ;;
        -p|--wakeup-server-port) WAKEUP_SERVER_PORT="$2"; shift ;;
        -t|--homeassistant-token) HOMEASSISTANT_TOKEN="$2"; shift ;;
        -u|--homeassistant-url) HOMEASSISTANT_URL="$2"; shift ;;
        -d|--dev-mode) DEV_MODE=true ;;
        -o|--homeassistant-offline-mode) HOMEASSISTANT_OFFLINE_MODE=true ;;
        -z|--zero-mq-server-url) ZERO_MQ_SERVER_URL="$2"; shift ;;
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

echo "Setting up local environment variables... in .env file"

echo "HOSTNAME=http://$HOSTNAME" > $DIRECTORY/../wakeup-server/.env
echo "PORT=$WAKEUP_SERVER_PORT" >> $DIRECTORY/../wakeup-server/.env
echo "HOMEASSISTANT_TOKEN=$HOMEASSISTANT_TOKEN" >> $DIRECTORY/../wakeup-server/.env
echo "HOMEASSISTANT_URL=$HOMEASSISTANT_URL" >> $DIRECTORY/../wakeup-server/.env
echo "HOMEASSISTANT_OFFLINE_MODE=$HOMEASSISTANT_OFFLINE_MODE" >> $DIRECTORY/../wakeup-server/.env
echo "ZERO_MQ_SERVER_URL=$ZERO_MQ_SERVER_URL" >> $DIRECTORY/../wakeup-server/.env
echo "DEV_MODE=$DEV_MODE" >> $DIRECTORY/../wakeup-server/.env

# For Docker .env.compose
echo "HOSTNAME=0.0.0.0" > $DIRECTORY/../wakeup-server/.env.compose
echo "PORT=$WAKEUP_SERVER_PORT" >> $DIRECTORY/../wakeup-server/.env.compose
echo "HOMEASSISTANT_TOKEN=$HOMEASSISTANT_TOKEN" >> $DIRECTORY/../wakeup-server/.env.compose
echo "HOMEASSISTANT_URL=$HOMEASSISTANT_URL" >> $DIRECTORY/../wakeup-server/.env.compose
echo "HOMEASSISTANT_OFFLINE_MODE=$HOMEASSISTANT_OFFLINE_MODE" >> $DIRECTORY/../wakeup-server/.env.compose
echo "ZERO_MQ_SERVER_URL=$ZERO_MQ_SERVER_URL" >> $DIRECTORY/../wakeup-server/.env.compose
echo "DEV_MODE=$DEV_MODE" >> $DIRECTORY/../wakeup-server/.env.compose

echo "Finished setting up local environment variables."
echo "    PORT=$WAKEUP_SERVER_PORT"
echo "    HOMEASSISTANT_URL=$HOMEASSISTANT_URL"
echo "    HOMEASSISTANT_OFFLINE_MODE=$HOMEASSISTANT_OFFLINE_MODE"
echo "    ZERO_MQ_SERVER_URL=$ZERO_MQ_SERVER_URL"
echo "    DEV_MODE=$DEV_MODE"

