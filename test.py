import pyvisa
import time

rm = pyvisa.ResourceManager()
# Will Print out a location of the Visa resource 
print(rm.list_resources())

# Configuration for 2220G-30-1 
dcps2157 = rm.open_resource("USB0::0x05E6::0x2220::9209773::INSTR")
dcps2157.baud_rate = 115200
print(dcps2157.query("*IDN?"))

# Configuration for DMM6500
dmm1934 = rm.open_resource("USB0::0x05E6::0x6500::04548310::INSTR") 
dmm1934.baud_rate = 115200
dmm1934.read_termination = '\r'
dmm1934.timeout = 5000
print(dmm1934.query("*IDN?"))


print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
# Sounds the Beeper for a 1/8th sec and Resets the system. 
print(dmm1934.query(":SYST:Time?"))
dmm1934.write(":SYSTem:BEEPer:IMMEdiate 300, .125; *RST")
dcps2157.write(":SYSTem:BEEPer:IMMEdiate 1800, 0.125; *RST")

for i in range(10):
    volt = "Source:voltage " + str(i)
    print(volt)
    dcps2157.write(volt)
    time.sleep(5)
    print(dmm1934.query(":MEAS:Volt?"))






