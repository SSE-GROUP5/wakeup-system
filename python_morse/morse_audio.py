import pyaudio
import time
import audioop
from morse_functions import decode_morse_letter
MAX_DASHES_FOR_DOT = 20

def calculate_volume_threshold(threshold):
  CHUNK = 1024
  FORMAT = pyaudio.paInt16
  CHANNELS = 1
  RATE = 44100
  RECORD_SECONDS = 10

  p = pyaudio.PyAudio()

  stream = p.open(format=FORMAT,
          channels=CHANNELS,
          rate=RATE,
          input=True,
          frames_per_buffer=CHUNK)

  total_letter = ''
  letter_timer = 0
  is_waiting = False
  END_WORD_TIME = 1

  for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    rms = audioop.rms(data, 2)    # here's where you calculate the volume

    # Convert RMS value to Morse code
    encoded_char = ''
    if rms > threshold:  # Set your desired threshold value
      encoded_char = '-'
    else:
      if len(total_letter) > 0 and total_letter[-1] == '-':
        encoded_char = ' '
        is_waiting = False

      if not is_waiting and len(total_letter) > 0 and total_letter[-1] == ' ':
        letter_timer = time.time()
        is_waiting = True

      if is_waiting and time.time() - letter_timer > END_WORD_TIME:
        encoded_char = '/'
        is_waiting = False

    total_letter += encoded_char

  stream.stop_stream()
  stream.close()
  p.terminate()

  return total_letter



def dashes_to_morse(morse_code):
  decode_word = ''
  dashes = morse_code.split(' ')
  for dash in dashes:
    if dash == '':
      decode_word += ' '
    elif len(dash) <= MAX_DASHES_FOR_DOT:
      decode_word += '.'
    else:
      decode_word += '-'

  return decode_word


def get_morse_letter(morse_code):
  morse_letter = ''
  words = morse_code.split(' /')
  for word in words:
    morse_letter += dashes_to_morse(word)
  return morse_letter





def main():
  threshold = 1400  # Set your desired threshold value
  total_letter = calculate_volume_threshold(threshold)
  morse_letter = get_morse_letter(total_letter)
  print(morse_letter)
  letter = decode_morse_letter(morse_letter)
  print(letter)


if __name__ == "__main__":
  main()