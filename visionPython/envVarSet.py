import json

# Reading the config file
with open('envVar.json', 'r') as file:
    config = json.load(file)

print("Program 1 - Read config:", config['CLOSED_EYES_FRAME'])

# Optionally modify the config
config['CLOSED_EYES_FRAME'] = 30

# Write the updated config back to the file
with open('envVar.json', 'w') as file:
    json.dump(config, file)
