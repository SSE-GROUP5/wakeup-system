import subprocess
import zmq
import json
import os



def closeSubprocess(subprocess):
    # Terminate the process
    subprocess.terminate()

    # Wait for the process to terminate
    subprocess.wait()

    # Check if the process has terminated
    if subprocess.poll() is not None:
        print("Process terminated.")
    else:
        print("Process is still running.")

def runSubProcess(script_path, config_path, socketPort):
    

    # Start the Python script using Popen
    currProcess = subprocess.Popen(['python', script_path])

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(socketPort)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    try:
        while True:
            topic, msg = socket.recv_multipart()
            print(f"Received on topic '{topic.decode('utf-8')}': {msg.decode('utf-8')}")

            msg = msg.decode('utf-8')
            topic = topic.decode('utf-8')

            if(topic == 'Camera'):
                
                json_data = json.loads(msg)

                closeSubprocess(currProcess)

                with open(config_path, "w") as outfile:
                    json.dump(json_data, outfile)

                currProcess = subprocess.Popen(['python', script_path])


    except Exception as e:
        print(f"Error: {e}")


runSubProcess('blinkDetect.py', 'config.json', "tcp://localhost:5556")