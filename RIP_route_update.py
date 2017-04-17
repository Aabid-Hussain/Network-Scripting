from all_paths import *

###### Create log file name with timestamp+filename ##############
testcase = "RIP route update"
filename = "log_" + testcase + ".log"
logger = logging_file(filename)


#### Start of Test case ###########################


log_print("Starting Test case %s" %testcase, 1)

###############Step 1: Open session with DUT, Route R1 and Router R2 ###########
DUT = th_init_device("C:/Python27/Automation/content/DUT.txt")
R1 = th_init_device("C:/Python27/Automation/content/R1.txt")
R2 = th_init_device("C:/Python27/Automation/content/R2.txt")


handler = th_open_dev(DUT)
if handler :
    setattr(DUT,'device_handler',handler)
    log_print("Step 1: Successfully open DUT at %s" %DUT.device_IP,1)
else :
    log_print("Step1: Failed to open DUT device at %s" %DUT.device_IP,1)
    exit

handler = th_open_dev(R1)
if handler :
    setattr(R1,'device_handler',handler)
    log_print("Step 1: Successfully open R1 at %s" %R1.device_IP,1)
else :
    log_print("Step1: Failed to open R1 device at %s" %R1.device_IP,1)
    exit

handler = th_open_dev(R2)
if handler :
    setattr(R2,'device_handler',handler)
    log_print("Step 1: Successfully open R2 at %s" %R2.device_IP,1)
else :
    log_print("Step1: Failed to open R2 device at %s" %R2.device_IP,1)
    exit
##################Step 2: Add IP address in DUT between R1 and R2 ###########
    
interface_list = [DUT.device_interface_1,DUT.device_interface_2]
ip_address_list = ['10.1.0.1','20.2.0.1']

if common_add_ip_address(DUT, interface_list, ip_address_list) :
    log_print("Step 2: Successfully Added IP %s to %s of DUT at %s" \
    %(ip_address_list, interface_list,DUT.device_IP),1)
else :
    log_print("Step2: Failed to add IP %s to %s of DUT at %s" \
    %(ip_address_list, interface_list,DUT.device_IP),1)
    exit
                
interface_list = [R1.device_interface_1, R1.device_interface_2, 'loopback0', 'loopback1','lo2']
ip_address_list = ['10.1.0.2', '12.1.2.2',]

if common_add_ip_address(R1, interface_list, ip_address_list) :
    log_print("Step 2: Successfully Added IP %s to %s of R1 at %s" \
    %(ip_address_list, interface_list,R1.device_IP),1)
else :
    log_print("Step2: Failed to add IP %s to %s of R1 at %s" \
    %(ip_address_list, interface_list,R1.device_IP),1)
    exit

                
interface_list = [R2.device_interface_1, R2.device_interface_2]
ip_address_list = ['20.2.0.2', '12.1.2.2']

if common_add_ip_address(R2, interface_list, ip_address_list) :
    log_print("Step 2: Successfully Added IP %s to %s of R2 at %s" \
    %(ip_address_list, interface_list,R2.device_IP),1)
else :
    log_print("Step2: Failed to add IP %s to %s of R2 at %s" \
    %(ip_address_list, interface_list,R2.device_IP),1)
    exit

##################Step 3: Configure OSPF on DUT and Add network towards R1 to area 0
#                          and network towards R2 to Area 1###########
dut_network_list_area0 = ['10.1.0.0']
dut_network_list_area1 = ['20.2.0.0']

dut_router_id = "0.0.0.0"

ospf_config_router_id(DUT, dut_router_id)

if ospf_add_networks(DUT, dut_network_list_area0, area = 0) :
    log_print("Step 3: Successfully Added Networks %s to DUT at %s in area 0" \
    %(dut_network_list_area0,DUT.device_IP),1)
else :
    log_print("Step3: Failed to add Networks %s to DUT at %s in area 0" \
    %(dut_network_list_area0,DUT.device_IP),1)
    exit
                
if ospf_add_networks(DUT, dut_network_list_area1, area = 1) :
    log_print("Step 3: Successfully Added Networks %s to DUT at %s in area 1" \
    %(dut_network_list_area1,DUT.device_IP),1)
else :
    log_print("Step3: Failed to add Networks %s to DUT at %s in area 1" \
    %(dut_network_list_area1,DUT.device_IP),1)
    exit
##################Step 4: Configure OSPF on R1 and Add network towards DUT to area 0
#                and network towards R2 to Area 0
R1_network_list = ['10.1.0.0','12.1.2.0']
R1_router_id = "1.1.1.1"
ospf_config_router_id(R1, R1_router_id)

if ospf_add_networks(R1, R1_network_list, area = 0) :
    log_print("Step 4: Successfully Added Networks %s to R1 at %s in area 0" \
    %(R1_network_list,R1.device_IP),1)
else :
    log_print("Step4: Failed to add Networks %s to R1 at %s in area 0" \
    %(R1_network_list,R1.device_IP),1)
    exit

##################Step 5: Configure OSPF on R2 and Add network towards R1 to area 0
#               and network towards DUT to Area 1
R2_network_list_area0 = ['12.1.2.0']
R2_network_list_area1 = ['20.2.0.0']                   

R2_router_id = "2.2.2.2"

ospf_config_router_id(R2, R2_router_id)

if ospf_add_networks(R2, R2_network_list_area0, area = 0) :
    log_print("Step 5: Successfully Added Networks %s to R2 at %s in area 0" \
    %(R2_network_list_area0,R2.device_IP),1)
else :
    log_print("Step5: Failed to add Networks %s to R2 at %s in area 0" \
    %(R2_network_list_area0,R2.device_IP),1)
    exit
                
if ospf_add_networks(R2, R2_network_list_area1, area = 1) :
    log_print("Step 5: Successfully Added Networks %s to R2 at %s in area 1" \
    %(R2_network_list_area1,R2.device_IP),1)
else :
    log_print("Step5: Failed to add Networks %s to R2 at %s in area 1" \
    %(R2_network_list_area1,R2.device_IP),1)
    exit

##### Step 6: Wait for interface to go to full state (sleep 40 sec)####################
log_print ("Waiting for 40 seconds for neighbour to reach full state",1)
time.sleep(40)

##### Step 7: Check DUT routing table has entry for destination R2 network
#                via intra route (R1) instead of inter area (R2)#######

dut_network = '12.1.2.0'

show_ip_route = common_get_ip_route(DUT)
if show_ip_route == "" :
    log_print("No Routing information",1)
    exit
else :
    log_print("Found Routing entry",1)

route_type= ospf_get_route_type(show_ip_route, dut_network)
if route_type == "" :
                   log_print(" Test Abort: No route entry",1)
                   exit
if not ospf_is_route_type_IA(route_type):
    log_print("TEST PASSED: Found Intra route",1)
else:
    log_print("TEST FAILED: Inter Area route found instead of intra area",1)
log_print( " ")
log_print( "End of Test Case %s" %testcase,1)
