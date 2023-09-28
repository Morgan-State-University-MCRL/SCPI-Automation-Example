import pyvisa
import time
import pandas as pd

rm = pyvisa.ResourceManager()
# Will Print out a location of the Visa resource 
print(rm.list_resources())

# Configuration for 2220G-30-1 
dcps = rm.open_resource("---") # Use NI Max to view the 
dcps.baud_rate = 115200
print(dcps.query("*IDN?"))

# Configuration for DMM6500
dmm = rm.open_resource("---") 
dmm.baud_rate = 115200
dmm.read_termination = '\n' # Gets rid of the \n when reading the values
print(dmm.query("*IDN?"))

print("~~~~~~~~~")

# Data Collection
voltages =  []

dmm.write(":SYSTem:BEEPer:IMMEdiate 300, .125; *RST")
dcps.write(":SYSTem:BEEPer:IMMEdiate 300, 0.125; *RST")
dcps.write("SOURce:OUTPut:STATe:ALL 1") # Turn on all inputs

for i in range(11): # from 0 - 10
    volt = "Source:voltage " + str(i)
    print(volt)
    dcps.write(volt)
    time.sleep(1) # Buffer to let DCPS to settle
    voltMeasurement =dmm.query(":MEAS:Volt?")
    voltages.append(voltMeasurement)
    print(voltMeasurement)

dcps.write("SOURce:OUTPut:STATe:ALL 0") # Turn off all inputs

# Data Processing

# Data table
d = {
     'Volt': voltages
 }

# Creating data table  
df = pd.DataFrame(data=d)
df.to_excel("output.xlsx")
print(df)