import netifaces
from socket import *

class NetioDiscover:
    def __init__(self, interface=None):
        self.devices = []
        if interface is None:
            self.interfaces = netifaces.interfaces()
        else:
            self.interfaces = interface
        print(self.interfaces)

    def getDevicesLinux(self, timeout=1):
        """
        Discover NETIO devices on all available network interfaces.
        Listen for defined timeout at avery interface and return Dictionary with found NETIO devices.
        Specific method for Linux operating system.
        """
        self.devices=[]
        outsocket = socket(AF_INET, SOCK_DGRAM)
        outsocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        outsocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        outsocket.bind(('', 62386))
        outsocket.settimeout(timeout)

        for keys in self.interfaces:
            try:
                print("sending to: %s" % keys)
                outsocket.setsockopt(SOL_SOCKET, 25, str(keys + '\0').encode('utf-8'))  # this is used to send and receive on all interfaces - need root privileges
                outsocket.sendto("01ec00".decode("hex"), ('255.255.255.255', 62387))
            except:
                print('Unable to send request')

            try:
                while True:
                    self.devices.append(self.parseDeviceInfo(outsocket.recvfrom(1024)[0]))
            except:
                continue


        return self.devices


    def parseDeviceInfo(self, data):
        """
        Parse NETIO Device information from data payload
        """
        binarydata = bytearray(data)

        if binarydata[0] is not 2:
            print('Data are not valid')
            return
        else:
            pass

        i=3
        params = []
        datalen=len(binarydata)
        while i < datalen-1:
            param = {'DATA': []}
            param['FTYPE'] = binarydata[i]
            i += 1
            paramlen = binarydata[i]
            i += 1
            if (i+paramlen) < len(binarydata):
                for j in range(0, paramlen):
                    param['DATA'].append(binarydata[i+j])
            i += paramlen
            params.append(param)

        device = {}

        for item in params:

            if item.get('FTYPE') == 0x01:   #FIRMWARE_VERSION
                device['fwversion'] = ''.join(chr(i) for i in item.get('DATA'))
                continue
            if item.get('FTYPE') == 0x02:   #MAC
                device['mac'] = ':'.join(format(i, 'x') for i in item.get('DATA')).upper()
                continue
            if item.get('FTYPE') == 0x03:   #IP
                device['ip'] = '.'.join(str(i) for i in item.get('DATA'))
                continue
            if item.get('FTYPE') == 0x04:   #NETMASK
                device['mask'] = '.'.join(str(i) for i in item.get('DATA'))
                continue
            if item.get('FTYPE') == 0x05:   #HOSTNAME
                device['hostname'] = ''.join(chr(i) for i in item.get('DATA'))
                continue
            if item.get('FTYPE') == 0x06:   #DHCP
                continue
            if item.get('FTYPE') == 0x07:   #SETUP_STATE
                continue
            if item.get('FTYPE') == 0x08:   #RESULT
                continue
            if item.get('FTYPE') == 0x09:   #PRODUCT
                device['model'] = ''.join(chr(i) for i in item.get('DATA'))
                continue
            if item.get('FTYPE') == 0x0a:   #MANUFACTURER
                device['manufacturer'] = ''.join(chr(i) for i in item.get('DATA'))
                continue
            if item.get('FTYPE') == 0x0b:   #PLATFORM
                device['platform'] = ''.join(chr(i) for i in item.get('DATA'))
                continue
            if item.get('FTYPE') == 0x0c:   #VARIANT
                device['hostname'] = ''.join(chr(i) for i in item.get('DATA'))
                continue
            if item.get('FTYPE') == 0x0d:   #TIMEOUT
                continue
            if item.get('FTYPE') == 0x0e:   #GATEWAY
                continue
            if item.get('FTYPE') == 0x0f:   #DNS
                continue
            if item.get('FTYPE') == 0x12:   #PRETTY_PLATFORM_NAME
                device['platformname'] = ''.join(chr(i) for i in item.get('DATA'))
                continue
            if item.get('FTYPE') == 0x13:   #DEVICE_NAME
                device['devicename'] = ''.join(chr(i) for i in item.get('DATA'))
                continue

        return device