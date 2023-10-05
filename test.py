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

# Data Preparation  
voltages =  [] # Data-to-read
resistances =[] #Data-to-calculate

# Data Collection
dmm.write(":SYSTem:BEEPer:IMMEdiate 300, .125; *RST")
dcps.write(":SYSTem:BEEPer:IMMEdiate 300, 0.125; *RST")
dcps.write("SOURce:OUTPut:STATe:ALL 1") # Turn on all inputs

# Data Processing (for data-to-read)
for i in range(11): # from 0 - 10
    volt = "Source:voltage " + str(i)
    print(volt)
    dcps.write(volt)
    time.sleep(1) # Buffer to let DCPS to settle
    voltMeasurement = float(format(dmm.query(":MEAS:Volt?"))) # Query the DMM for volts, format out of sci-not up to 6 sigfigs (default), if its a string turn into float var  
    voltages.append(voltMeasurement)
    print(voltMeasurement)

dcps.write("SOURce:OUTPut:STATe:ALL 0") # Turn off all inputs

# Data Processing (for data-to-calculate)
for v in voltages: # from 0 - 10
    resistance = v/.05 # .05 amps hypothetically 
    print(resistance)
    resistances.append(resistance)

# Data table
voltsData = pd.DataFrame({
    'Volts': voltages})
ohmsData = pd.DataFrame({
    'Resistances':resistances})

# Creating data table  
totalData = pd.concat([voltsData,ohmsData], axis=1)
totalData.to_excel("output.xlsx")
print(totalData)