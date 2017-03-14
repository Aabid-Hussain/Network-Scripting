# NetworkAutomationUsingPython
The idea was inspired from ClosedFlow: OpenFlow-like Control over Proprietary Devices, which allows enterprises to control the network through a centralized controller by using Python scripts, which is able to send and receive configurations and information from all managing boxes in the network without entering authentication information to login to each box. The program requires an MS Excel file that contains authentication information of the managing boxes including Name, IP address, Username, and Password.

Author: Pavan Kumar Reddi

**Reference**: 
Hand, Ryan, and Eric Keller. "ClosedFlow: openflow-like control over proprietary devices." In Proceedings of the third workshop on Hot topics in software defined networking, pp. 7-12. ACM, 2014.

Byers, Kirk. "Python for Network Engineers." Python for Network Engineers. Accessed April 22, 2015. https://pynet.twb-tech.com/.

### How do I get set up? ###

**Summary of set up**: Python 2.7.9 and the xlrd module (a Python module for extracting data from MS Excel files) are required to run this program. The program contains four python scripts and an excel file with switch's information:

* main_program.py - the main script of the program combining all modules

* network_automation.py - automation happens here!

* telnet_connection.py - a module that creates a telnet connection to the managing boxes

* cisco_config.py - an interactive configuration program for cisco configuration

* open_excel_file.py - a module that gets data from MS Excel files

* switch_list.xlsx - a MS Excel file containing data of switches (Name, IP address, Username, and Password)

**How to run tests**: Open Command Prompt for Windows or Terminal for Mac/Linux. Go to the folder where files locate. Then run this command:

```
#!python

python main_program.py
```
