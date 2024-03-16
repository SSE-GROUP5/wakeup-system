import socket
import wakeonlan
import binascii
import os

def wol(mac, ip, port=9):
    wakeonlan.send_magic_packet(mac, ip_address=ip, port=port)

def validate_mac_address(mac): 
    mac = mac.replace(':', '')
    mac = mac.replace('-', '')
    return mac

def create_magic_packet(mac):
    mac = validate_mac_address(mac)
    if len(mac) != 12:
        raise ValueError('Incorrect MAC address format')
    magic_packet = 'FF'*6 + str(mac)*16
    data_sent = binascii.unhexlify(magic_packet)                               
    return mac,data_sent

def change(ip):
    ip_list = ip.split('.')
    broadcast_ip = ip_list[0] + '.' + ip_list[1] + '.' + ip_list[2] + '.255'
    return broadcast_ip

def packet_sent(mac, ip, port):
    broadcast = change(ip)
    formatted_mac, send_data = create_magic_packet(mac)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(send_data, (broadcast, port))
    s.close()

if __name__ == "__main__":  
    print('Waking up target device')
    mac = os.environ.get('mac','11:22:33:44:55:66')
    #change to fit your mac address
    ip = os.environ.get('ip','111.222.0.33')
    #change to fit your private ip address
    port = os.environ.get('port',9)

    packet_sent(mac,ip,port)