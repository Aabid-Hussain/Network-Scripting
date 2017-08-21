import pyshark
import time

'''
capture = pyshark.FileCapture("E:\ME\Lab\RIP\Rip.pcapng")

for inputline in capture:
    print inputline
    time.sleep(10)



#capture = pyshark.LiveCapture(interface= 'Loopback')
capture = pyshark.RemoteCapture('2.2.2.2',
                 'Loopback',remote_port= 23)
capture.sniff(timeout=50)

for packet in capture.sniff_continuously(
        packet_count= 5):
    print("Just arrived: {}".format(packet))

'''

capture = pyshark.FileCapture("E:\ME\Lab\RIP\BGP_routes.pcapng")

for inline in capture:
    print (inline)
    time.sleep(5)
