from wakeonlan import send_magic_packet


devices = {
   'pc':{'mac':'MAC_ADRESS','ip_address':'IP_ADRESS'}
}

def wake_device(device_name):
   if device_name in devices:
      mac,ip = devices[device_name].values()
      send_magic_packet(mac,ip_address=ip)
      print('Magic Packet Sent')
   else:
      print('Device Not Found')