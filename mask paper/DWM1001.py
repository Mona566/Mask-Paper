#DWM Serial Parser by Brian H. | Updated 3/6/19
import serial
import time
import datetime


DWM=serial.Serial(port="/dev/serial0", baudrate=115200) # open serial port
print("Connected to " +DWM.name) # check which port was really used
DWM.write("\r\r".encode()) # two carriage returns to initiate communication with Decawave tag
time.sleep(1)
DWM.write("lec\r".encode()) # tell Decawave board to start sending data
# The usage of lec: how distances to ranging anchors and the position if location engine is enabled in CSV format.
#Sending this command multiple times will turn on/off this functionality.
time.sleep(1)
while True:
    try:
        line=DWM.readline() #ead one line from serial device.
        # first number after AN0 is the anchor ID. Second, third, and fourth numbers are the (x,y,z) initialized positions of the anchors,
        #  and the fifth number is measured position.
        if(line): 
            parse=line.decode().split(",")
            if parse[0]=="DIST":
                pos_AN0=(parse[parse.index("AN0")+2],parse[parse.index("AN0")+3],parse[parse.index("AN0")+4])
                dist_AN0=parse[parse.index("AN0")+5]
                print(datetime.datetime.now().strftime("%H:%M:%S"),pos_AN0,":",dist_AN0)
            else:
                print("Distance not calculated: ",line.decode())
    except Exception as ex:
        print(ex)
        break
DWM.write("\r".encode())
DWM.close()