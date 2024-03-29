import pyvisa
import time
import pandas as pd
import numpy as np

rm = pyvisa.ResourceManager()
# Will Print out a location of the Visa resource 
# print(rm.list_resources())

# Machine to talk to
machine = rm.open_resource("USB0::0x0699::0x03C7::C023303::INSTR") # Use NI Max to view the 
machine.baud_rate = 115200
# print(machine.query("*IDN?"))
# print(machine.query("MEASUREMENT:MEAS1:mean?"))
machine.write("MEASUrement:IMMed:TYPe Phase")
print(machine.query(" MEASUrement:IMMed:VALue?"))
# machine.write("*RST")
# machine.write("HORIZONTAL:DELay:SCALE 2E-3") 
# 2E-3, 100E-6, 1E-6
# Query 
# machine.write("MEASUrement:IMMed:SOUrce1 CH1")
# Write
# machine.write("ACQUIRE:STATE ON")
# machine.write("MEASUREMENT:IMMED:TYPE AMPLITUDE")
# print(machine.query("MEASUrement:MEAS1:mean?"))
