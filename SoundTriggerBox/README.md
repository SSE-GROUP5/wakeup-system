# SoundsTriggerBox
SoundsTriggerBox is a voice-assistant application designed to empower individuals with Amyotrophic Lateral Sclerosis (ALS) or Motor Neurone Disease (MND) through sound recognition. Recognizing that vocal abilities vary greatly among individuals with ALS or MND, SoundsTriggerBox allows users to train the system to recognize their unique sound profile, ensuring adaptability to diverse vocal characteristics. The application leverages Vosk for speech recognition and PyAudio for capturing sound. In emergency situations, when a predefined sound trigger is detected, the system can send an alert via SMS using the integrated Twilio API. This project, developed in Python with a user-friendly tkinter graphical interface, is positioned as a vital tool to enhance safety and independence for individuals living with ALS or MND by providing a hands-free, voice-activated emergency response system.

To run SoundsTriggerBox service:

1. Clone the repo: git clone https://github.com/zcabzfe/SoundsTriggerBox.git

2. Make sure you have Python installed. If not, please install python by following this guide: https://realpython.com/installing-python/

3. Install requirements.txt. Run "pip install -r requirements.txt" in the terminal.(To download a particular package, such as Vosk, simply enter "pip install vosk" into your command prompt or terminal. This will automatically download the latest version of the package, irrespective of the version specified.)

4. Check your microphone status and give Python access to your microphone:

   - On Windows, you can do this through the Settings app: Go to 'Start' > 'Settings' > 'Privacy' > 'Microphone', and make sure Python is checked. If you have multiple microphones, you can select and apply the one to use as the default in 'Windows system' > 'Control Panel' > 'Hardware and Sound' > 'Hardware and Sound' > 'Manage audio devices' > 'Recording'.
   
   - On macOS, go to 'System Preferences' > 'Security & Privacy' > 'Microphone', and make sure Python is checked to allow it to access the microphone.

5. Run the main.py.

6. Enter correct Twilio account details (If you do not have a Twilio account yet, please follow this guide from 2:01 to 3:00: https://www.youtube.com/watch?v=ywH2rsL371Q)

7. Follow instructions to Train your sound profile.

8. Start SoundTriggerBox Service (Say "stop" or click on "Stop SoundTriggerBox Service" to stop the service or "Quit" to quit the program).

Note: If your microphone is not working or Python does not have access to the microphone on your computer, you may encounter issues while running SoundsTriggerBox. Make sure your microphone is functioning correctly and Python has necessary permissions before proceeding.


