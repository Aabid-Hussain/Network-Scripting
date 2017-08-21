#A program to find route in route table

import re

Hash_line = "*#"*5

show_output = """RTB# show ip route
Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP
 D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
 N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
 E1 - OSPF external type 1, E2 - OSPF external type 2
 i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
 * - candidate default, U - per-user static route, o - ODR
 P - periodic downloaded static route
Gateway of last resort is not set
 2.0.0.0/24 is subnetted, 1 subnets
C 2.2.2.0 is directly connected, Ethernet0/0
C 3.0.0.0/8 is directly connected, Serial1/0
O N2 200.1.1.0/24 [110/94] via 2.2.2.1, 00:11:12, Ethernet0/0
O N1 200.2.2.0/24 [110/20] via 2.2.2.2, 00:12:23, Ethernet0/0
 131.108.0.0/24 is subnetted, 2 subnets
O IA 141.108.1.0 [110/84] via 2.2.2.1, 00:12:11, Ethernet0/0
O IA 151.108.1.0 [110/84] via 2.2.2.1, 00:12:11, Ethernet0/0
O 131.108.2.0 [110/74] via 2.2.2.2, 00:12:23, Ethernet0/0
O IA 131.108.1.0 [110/84] via 2.2.2.2, 00:12:11, Ethernet0/0"""

def Search_OSPF_Route():#Type_Of_Route, Network_Address, Gateway_Address):
    global show_output
    net,gateway =[],[]
    Type_Of_Route = 'O'
    regex = r"^%s\s([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)" \
            ".*([0-9]+\.[0-9]+\.[0-9]+\.[0-9])" \
            %Type_Of_Route

    for lines in show_output.split('\n'):
        #print(lines)
        matches = re.search(regex,lines)
        if matches:
            net.append(matches.group(1))
            gateway.append(matches.group(2))
            print "Network: {} is present in Route Table".format(net)
            print "Gateway: {} is present in Route Table".format(gateway)


 #           print "%s Type of Route with network %s and gateway %s is not found" %(Type_Of_Route,Network_Address, Gateway_Address)

print (Hash_line)
#
# Route_Type = raw_input("Enter the Type of Route: ")
# Network = raw_input("Enter the Network address: ")
# Gateway = raw_input("Enter the Gateway address:")

#Search_OSPF_Route(Route_Type,Network,Gateway)
Search_OSPF_Route()






