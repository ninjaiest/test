import socket
import sys

addr = sys.argv[1]
port = int(sys.argv[2])

password = raw_input("please input the password:")

# use tcp mode
# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# s.connect((addr, port))

# use udp mode
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.sendto(password, (addr, port))
reply = s.recv(4096)
print reply

s.close()
sys.exit()
