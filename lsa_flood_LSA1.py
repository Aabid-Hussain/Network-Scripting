#!c:\Python27\python
####################################################################
#  Testscript: ts_ospf_func_lsa_flooding_type1.py
#  Purpose  :  To verify that DUT distribute LSA type 1 within the area
#               it belong to.
#
#  Detail   : The DUT when configured to be in an area, sends and receives
#             LSA type 1 
#
#  Steps    :
#       Step 1: Open session with DUT and Router R2
#       Step 2: Add IP address between DUT and R2
#       Step 3: Add loopback and IP address on DUT and R2
#       Step 4: Configure OSPF and Add network on DUT and R2
#       Step 5: Check if DUT sends its networks to R2 as LSA1 
#
####################################################################

##############Import main module with all paths ########
from all_paths import *

###### Create log file name with timestamp+filename ##############
testcase = "ospf_func_lsa_flooding_type1"
filename = "log_" + testcase + ".log"
logger = logging_file(filename)


#### Start of Test case ###########################


log_print("Starting Test case %s" %testcase, 1)

###############Step 1: Open session with DUT and Router R2 ###########
DUT = th_init_device("C:/Python27/th_automation/resource/R1.txt")
R2 = th_init_device("C:/Python27/th_automation/resource/R2.txt")

handler = th_open_dev(DUT)
if handler :
    setattr(DUT,'device_handler',handler)
    log_print("Step 1: Successfully open DUT at %s" %DUT.device_IP,1)
else :
    log_print("Step1: Failed to open DUT device at %s" %DUT.device_IP,1)
    exit

handler = th_open_dev(R2)
if handler :
    setattr(R2,'device_handler',handler)
    log_print("Step 1: Successfully open R2 at %s" %R2.device_IP,1)
else :
    log_print("Step1: Failed to open R2 device at %s" %R2.device_IP,1)
    exit

##################Step 2: Add IP address between DUT and R2 ###########
    
interface_list = [DUT.device_interface_1]
ip_address_list = ['12.1.2.1']

if common_add_ip_address(DUT, interface_list, ip_address_list) :
    log_print("Step 2: Successfully Added IP %s to %s of DUT at %s" \
    %(ip_address_list, interface_list,DUT.device_IP),1)
else :
    log_print("Step2: Failed to add IP %s to %s of DUT at %s" \
    %(ip_address_list, interface_list,DUT.device_IP),1)
    exit
                
interface_list = [R2.device_interface_1, R2.device_interface_2]
ip_address_list = ['12.1.2.2', '23.2.3.2']

if common_add_ip_address(R2, interface_list, ip_address_list) :
    log_print("Step 2: Successfully Added IP %s to %s of R2 at %s" \
    %(ip_address_list, interface_list,R2.device_IP),1)
else :
    log_print("Step2: Failed to add IP %s to %s of R2 at %s" \
    %(ip_address_list, interface_list,R2.device_IP),1)
    exit

##################Step 3: Add loopback and IP address on DUT and R2###########

interface_list = ['loopback 1', 'loopback 2', 'loopback 3']
ip_address_list = ['10.1.1.1','10.2.1.1','10.3.1.1']

if common_add_ip_address(DUT, interface_list, ip_address_list) :
    log_print("Step 3: Successfully Added IP %s to %s of DUT at %s" \
    %(ip_address_list, interface_list,DUT.device_IP),1)
else :
    log_print("Step3: Failed to add IP %s to %s of DUT at %s" \
    %(ip_address_list, interface_list,DUT.device_IP),1)
    exit
                
interface_list = ['loopback 1', 'loopback 2', 'loopback 3']
ip_address_list = ['20.1.1.1','20.2.1.1','20.3.1.1']

if common_add_ip_address(R2, interface_list, ip_address_list) :
    log_print("Step 3: Successfully Added IP %s to %s of R2 at %s" \
    %(ip_address_list, interface_list,R2.device_IP),1)
else :
    log_print("Step3: Failed to add IP %s to %s of R2 at %s" \
    %(ip_address_list, interface_list,R2.device_IP),1)
    exit

##################Step 4: Configure OSPF and Add network on DUT and R2###########
dut_network_list = ['12.1.2.0','10.1.1.0','10.2.1.0','10.3.1.0']
R2_network_list = ['12.1.2.0','20.1.1.0','20.2.1.0','20.3.1.0']

dut_router_id = "1.1.1.1"
R2_router_id = "2.2.2.2"

ospf_config_router_id(DUT, dut_router_id)
ospf_config_router_id(R2, R2_router_id)

if ospf_add_networks(DUT, dut_network_list, area = 1) :
    log_print("Step 4: Successfully Added Networks %s to DUT at %s" \
    %(dut_network_list,DUT.device_IP),1)
else :
    log_print("Step4: Failed to add Networks %s to DUT at %s" \
    %(dut_network_list,DUT.device_IP),1)
    exit
                

if ospf_add_networks(R2, R2_network_list, area = 1) :
    log_print("Step 4: Successfully Added Networks %s to R2 at %s" \
    %(R2_network_list,R2.device_IP),1)
else :
    log_print("Step4: Failed to add Networks %s to R2 at %s" \
    %(R2_network_list,R2.device_IP),1)
    exit

##################Step 5: Check if DUT sends its networks to R2 as LSA1###########
adv_router = dut_router_id
##### Wait for neighbour to reach full state ####################
log_print ("Waiting for 40 seconds for neighbour to reach full state",1)
time.sleep(40)

Lsa1_list = ospf_get_lsa_type1(R2, adv_router)
dut_network_list = ['10.1.1.1','10.2.1.1','10.3.1.1']



if ospf_check_list_in_list(dut_network_list, Lsa1_list) :
    log_print("TEST PASSED: Step 5: DUT Sends its network to R2 at %s" \
    %(R2.device_IP),1)
else :
    log_print("TEST FAILED: Step 5: DUT did not sends its network to R2 at %s" \
    %(R2.device_IP),1)

log_print( " ")
log_print( "End of Test Case %s" %testcase,1)

