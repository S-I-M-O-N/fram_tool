
import serial,time #You need the pyserial library
import struct      #For packing data into bytes

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0)
#time.sleep(10);#my arduino bugs if data is written to the port after opening it
#romsize=1024 # Size in byte

print("  original delevopment by")
print("  Robson Couto 2016")
print("  www.dragaosemchama.com.br")
print("  github.com/robsoncouto/eprom\n")
print("  modified by S-I-M-O-N 2021")
print("  github.com/S-I-M-O-N/fram_tool\n")

#Default value, 32kB chip:
powerof2=5
romsize=(2**powerof2)*1024
numsectors=int(romsize/128) # I am sending data in 128 byte chunks


while True:

    print("  What would you like to do?      ")
    print("                                  ")
    print("          1-Read FRAM             ")
    print("          2-burn FRAM             ")
    print("                                  ")
    print("          4-blank check           ")
    print("          5-select chip size [",int(romsize/1024),"kB ]")
    print("          6-verify FRAM           ")
    print("                                  ")
    print("          7-quit                \n")
    #get option from user:
    option=int(input("Please insert a number: "))

    #Read EPROM
    if(option==1):
        name=input("What the name of the file? ")

        f = open(name, 'w')
        f.close()
        ser.flushInput()
        ser.write(b"\x55")
        ser.write(bytes("r","ASCII"))
        ser.write(powerof2.to_bytes(1, 'big'))
        numBytes=0
        f = open(name, 'ab')
        #I just read the data and put it into a file.
        #TODO - Checksum scheme as when burning
        while (numBytes<romsize):
            while ser.inWaiting()==0:
                print("Reading from FRAM. Current percentage:{:.2%}".format(numBytes/romsize),end='\r')
                time.sleep(0.1)
            data = ser.read(1)#must read the bytes and put in a file
            f.write(data)
            numBytes=numBytes+1
        f.close()
        print("\nDone\n")
    #Burn EPROM, see schematic at my website
    if(option==2):
        name=input("What's the name of the file? ")
        print(name)
        f = open(name, 'rb')
        for i in range(numsectors):
            ser.write(b"\x55")
            ser.write(bytes("w","ASCII" ))
            time.sleep(0.001)
            #send address of the block first
            ser.write(struct.pack(">B",i>>8))
            CHK=i>>8
            time.sleep(0.001)
            ser.write(struct.pack(">B",i&0xFF))
            CHK^=i&0xFF
            time.sleep(0.001)
            data=f.read(128);
            #print(data)

            #Gets checksum from xoring the package
            for j in range(len(data)):
                 CHK=CHK^data[j]
            time.sleep(0.001)
            print("Writing data. Current percentage:{:.2%}".format(i/numsectors),end='\r')
            #print("CHK:", CHK)
            response=~CHK

            #keeps trying while the replied checksum is not correct
            while response!=CHK:
                ser.write(data)
                ser.write(struct.pack(">B",CHK&0xFF))
                timeout=30
                while ser.inWaiting()==0:
                    time.sleep(0.01)
                    timeout=timeout-1
                    if timeout==0:
                        print("could not get a response, please start again\n")
                        break
                response=ord(ser.read(1))
                if response!=CHK:
                    print("wrong checksum, sending chunk again\n")
        f.close()

    #Just some info
#    if(option==3):
#
#        print("\nA more detailed write up about this project is available at www.dragaosemchama.com.br")
#        print("This script goes together with a Arduino sketch, both are used to read and program")
#        print("eproms on the cheap.")
#        print("Written by Robson Couto\n")
 
   #Blank check
    if(option==4):
        #same as reading
        ser.flushInput()
        ser.write(b"\x55")
        ser.write(bytes("r","ASCII"))
        ser.write(powerof2.to_bytes(1, 'big'))
        numBytes=0
        blank=1
        while (numBytes<romsize):
            while ser.inWaiting()==0:
                print("Reading from FRAM. Current percentage:{:.2%}".format(numBytes/romsize),end='\r')
                time.sleep(0.1)
            data = ser.read(1)
            numBytes=numBytes+1
            if ord(data)!=255:
                blank=0
                break
        #Ends check on first byte not erased
        if blank==1:
            print("\nThe chip is blank\n")
        else:
            print("\nThe chip seems to contain data\n")
        print("Done\n")
    #Change size of EPROM, for reading EPROMs other than 1MB
    if(option==5):
        print("Current FRAM size:",int(romsize/(1024)),"kB\n")
        kilos=float(input("Please insert the size of the FRAM in Kilobytes: "))
        romsize=kilos*1024
        numsectors=int(romsize/128) # I am sending data in 128 byte chunks
        #if kilos>1:
        for x in range(11):
            if 2 ** x == kilos :
                powerof2 = x
                print("FRAM size changed to ",int(2 ** powerof2),"kB\n")
                break
            elif x == 10:
                romsize=32*1024
                print("FRAM size invalid. Only powers of 2 up to 1MB allowed\n")

        #else:
        #    print("Eprom size changed to ",int(romsize/(1024)),"kB\n")
    #This is for checking if the eprom was programmed right
    if(option==6):
        #Reads each byte and compares with a byte in the file
        print("This compares a FRAM with a file in the script folder\n")
        name=input("\nWhat's the name of the file?\n")
        f = open(name, 'rb')
        ser.flushInput()
        ser.write(b"\x55")
        ser.write(bytes("r","ASCII"))
        ser.write(powerof2.to_bytes(1, 'big'))
        numBytes=0
        while (numBytes<romsize):
            while ser.inWaiting()==0:
                print("Reading from FRAM. Current percentage:{:.2%}".format(numBytes/romsize),end='\r')
                time.sleep(0.01)
            eprom_byte = ser.read(1)
            file_byte = f.read(1)
            if(eprom_byte!=file_byte):
                #the \033[031m and \033[0m sequence are ansi sequences that turn text red and cancel it respectively
                #I dont know how windows handle them
                print("\n\033[31mFound mismatch at",hex(f.tell()))
                print("- FRAM byte:",hex(ord(eprom_byte)),"- file byte:",hex(ord(file_byte)),"\033[0m\n")
            numBytes=numBytes+1
        print("\nDone\n")
    if(option==7):
        print("See ya!")
        break
