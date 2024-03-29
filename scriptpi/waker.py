import socket, struct

class Waker():
    def makeMagicPacket(self, macAddress):
        # Take the entered MAC address and format it to be sent via socket
        splitMac = str.split(macAddress,':')
    
        # Pack together the sections of the MAC address as binary hex
        hexMac = struct.pack('BBBBBB', int(splitMac[0], 16),
                             int(splitMac[1], 16),
                             int(splitMac[2], 16),
                             int(splitMac[3], 16),
                             int(splitMac[4], 16),
                             int(splitMac[5], 16))
    
        self.packet = b'\xff' * 6 + hexMac * 16 #create the magic packet from MAC address
    
    def sendPacket(self, packet, destIP, destPort = 7):
        # Create the socket connection and send the packet
        s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(packet,(destIP,destPort))
        s.close()
        
    def wake(self, macAddress, destIP, destPort=7):
        self.makeMagicPacket(macAddress)
        self.sendPacket(self.packet, destIP, destPort)
        