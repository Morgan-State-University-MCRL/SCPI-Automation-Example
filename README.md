# Morgan State Mechatronics Laboratory SCPI Automation (OS: Windows) 
Still in process of writing...

Last Updated 9/27/23

## Synopsis
Being able to automating the test equipment in the lab can help speed up  projects. This Repository of code and tutorials aims to help jump start others into being able to automate their labs. 

The only thing you need is a USB splitter and the according amount of USB-B to -A cables to how many machines you plan on using. You may not need a splitter, but considering how laptops are made nowadays, yeah. Ask Mr. Anthony if he's around, and he can lend you the cables. Also you can ask me, Ethan, to use my USB splitter if you want. Mine is USB-A FYI. 

This program will be able to collect data points from machines and output them into and excel file called *output.xlsx*

### Instrument Setup
The test script here uses a DMM6500 and a 2220G-30-1 DCPS. It should change the values of the DCPS in increments of one from 0 to 10. The DCPS should be wired on channel 1 to the front panel input of the DMM. Red to red, black to black. The USBs should be connecting the instruments to the computer running the script through whatever practical means. 

## Installing Prerequisite Software
Assuming you are already using a text editor such as VSC (recommended) or the one Jetbrains made, you are ready. Most of this section will be redirecting to other  tutorials. 

### Installing Git (Version Control and cloud back ups)
See https://git-scm.com/downloads

### Installing NI Visa 
A backend software suite from National Instruments. Look up "NI Visa" and you should see the option to choose OS and the verion. The version will be dictated by the Quarter of the year (2023 Q1, 2024 Q4, etc.) It doesn't matter just install the latest one. 

### Installing Python
See https://www.python.org/downloads/

## Configuring Python

At this point, is best to `git pull` this repository. Go to the folder where you want to store this repository. 

>`git init` 

>`git pull https://github.com/Morgan-State-University-MCRL/SCPI-Automation-Example.git`

### Creating Virtual Environment (Optional but recommended)

>`py -m venv env`

>`.\env\Scripts\activate`

### Installing python packages
 The *req.txt* file is a file that pip (the python package manager) can read from to make life easy for you. 

 >`py -m pip install -r req.txt`
 
 The main packages being installed are
 
 - VISA (The communicator)
 - pyVisa (The backup communicator)
 - NumPy (Scientific calculator of sorts)
 - Pandas (Database manager and visualizer)


## How to Use Software

### Configuring Instruments

***Make sure the DMM6500 you are using is configured for SCPI. Everything else is SCPI by default.***

#### Obtaining VISA Resource Name (VRN) 
##### ALL READ THE STEPS FIRST... Then Execute
1. Open NI MAX
2. When it opens, you are going to want to hit the refresh button. Nothing will happen, but thats ok. 
3. On the left side of NI MAX, should see a drop down bar for *devices and interfaces*. Click it.
4.  When you do that an error may come up. (It always happens for me). Its talking something about the MAX database not running. ignore it. close it out.
5. Look back at the left side of NI MAX, and you should see the device names of the instruments that you plugged in.
6. Click on one of the devices referenced there. At the bottom you should see a label called "VISA Resource Name".

That string of characters should be copy-pasted into its respective instrument being referenced in the code where it says `---`. 

### Running the python Script

 Enter the VRNs and press GO  

## Tips and Reminders

## References

Tektronics https://www.tek.com/en/documents/technical-brief/getting-started-with-oscilloscope-automation-and-python

