# Smart Wake up System 
This project is designed to:
- **Reduce** number of calls made to nurses.
- **Facilitate** Patient interactions with its environment.
- **Enhance** nurse response for emergency situations.
## System Architecture
![Wakeup_Architecture_2024](https://github.com/SSE-GROUP5/wakeup-system/assets/75443246/c4981149-324d-4bcc-b136-89e019463d0e)

The system is divided into 3:
- **Triggers** - the defined triggers (e.g. fall detection or sound detection) are monitored by camera and microphone.
- **Target devices** - Devices that are controlled by the system (e.g. homeAssitant, LAN, Telegram chat).
- **WakeUp system** - acts as a controller to map the triggers to the target device. Mapping is controlled from MFC GUI.

## Folder structure
- **audio_classification** - classifies the audio (snaps, knocks etc), which is used to trigger the smart devices.
- **beepy** - This is a variant of the original beepy library [beepy-v1](https://github.com/prabeshdhakal/beepy-v1) that is used to warn the patient that a trigger is currently reading the environment.
- **fall_detection** - tracks the upper body angle, and used to detect a fall, which is used to trigger emergency situation and send alert to nurse.
- **fall_detection_standing** - tracks the full body, and used to detect a fall, which is used to trigger emergency situation and send alert to nurse. Orignal code from [here](https://github.com/bakshtb/Human-Fall-Detection)
- **morse_vision** - uses blink detection to convert it into morse code, which is used to trigger the smart devices.
- **morse_audio** - uses the amplitude of a voice to convert it into morse code.
- **telegram_bot** - sends the alert to a telegram channel via a bot.
- **wakeonlan** - wakes up the target device with the wake on lan protocol.
- **python_blinking** - detects the eyes blinking, which is used to trigger smart devices.
- **wakeup_server** - the controller, that maps the **triggers** to the **target devices**.
- **whisper** - real time speech transcription, to trigger emergency and non-emergency situtations.
- **zeromq** - custom module to update on the run the triggers from the wakeup server with zeroMQ.

### In Collaboration with:
<img src="https://github.com/SSE-GROUP5/wakeup-system/assets/75443246/3d45fe59-2177-4196-bb57-3a379a42c639" width="150" height="70">   <img src="https://github.com/SSE-GROUP5/wakeup-system/assets/75443246/518844b3-1d2d-444c-9d2b-7f4dda07b68b" width="150" height="100">   <img src="https://github.com/SSE-GROUP5/wakeup-system/assets/75443246/b1212966-1e4d-450b-ac4f-4fb994acf488" width="180" height="100">    <img src="https://logospng.org/download/roche/roche-4096.png" width="180" height="120">



