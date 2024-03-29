import pyvisa
import time
import pandas as pd
import numpy as np

rm = pyvisa.ResourceManager()
# Will Print out a location of the Visa resource 
print(rm.list_resources())

# Configuration for AFG1062
osp = rm.open_resource("USB0::0x0699::0x0353::2328092::INSTR") # Use NI Max to view the 
osp.baud_rate = 115200
print(osp.query("*IDN?"))

# Configuration for TBS2000B
fg = rm.open_resource("USB0::0x0699::0x03C7::C023303::INSTR") 
fg.baud_rate = 115200
fg.read_termination = '\n' # Gets rid of the \n when reading the values
print(fg.query("*IDN?"))
print("~~~~~~~~~")

# Data Preparation  
frequencies =  []

for hertz in range(21):
    frequencies.append(round(hertz,2))
    print(frequencies)



measFreq = [] 
p2p = [] 
amplitude = [] 

# Data Collection
osp.write(":SYSTem:BEEPer:IMMEdiate 300, .125; *RST")
fg.write(":SYSTem:BEEPer:IMMEdiate 300, 0.125; *RST")
fg.write("SOURce:OUTPut:STATe:ALL 1") # Turn on all inputs

# Data Processing (for data-to-read)
for hz in frequencies: # from 0 - 10
    fg.write("Source1:freq:fixed " + str(hz)+"khz")
    print(str(hz) + "khz")
    time.sleep(1) # Buffer to let DCPS to settle
    freqMeasurement = (format(osp.query("MEASUREMENT:MEAS1:TYPE FREQUENCY?"))) # Query the DMM for volts, format out of sci-not up to 6 sigfigs (default), if its a string turn into float var  
    print(freqMeasurement)

fg.write("SOURce:OUTPut:STATe:ALL 0") # Turn off all inputs

# Data Processing (for data-to-calculate)


# # Data table
# voltsData = pd.DataFrame({
#     'Volts': voltages})
# ohmsData = pd.DataFrame({
#     'Resistances':resistances})

# # Creating data table  
# totalData = pd.concat([voltsData,ohmsData], axis=1)
# totalData.to_excel("output.xlsx")
# print(totalData)