import sendgrid
import os
from sendgrid.helpers.mail import *
import numpy as np

class MailClient():
    
    def __init__(self, primary_test_device, sendgrid_api_key, mail_to_users):
        print "Initializing email"
        self.sendgrid_api_key = sendgrid_api_key
        self.mail_to_users = mail_to_users
        self.primary_test_device = primary_test_device

    def build_email(self, feature):

        message_body = self.build_feature_html(feature)
        message_body += self.build_scenario_html(feature["scenarios"])

        return message_body

        

    def build_feature_html(self, feature):
        scenarios = feature["scenarios"]
        body = ""

        body += "<div id='bodyDiv' style='font-family : Trebuchet MS'>"
        body += "<h3>Device Info:</h3>"

        device_info = scenarios[scenarios.keys()[0]]["users"]["Ellie"]['device_info']
        if (len(device_info) > 0 ) :
            body += "<table width='20%' style='font-family : Trebuchet MS'>"
            for key,value in device_info.iteritems():
                body += "<tr>"
                body += "<td style=' text-align:left ; color: black;  background :#D3D3D3' >"+ key+"</td>"
                body += "<td style=' text-align:left ; color: black;  background :#D3D3D3' >"+ str("{0:.2f}".format(np.mean(value)) if isinstance(value,list) else value) + "</td>"
                body += "</tr>"
            body += "</table><br/><br/><br/>"

        body += "<h3>Summary:</h3>"

        body += "<table width='20%' style='font-family : Trebuchet MS'>"
        body += "<tr>"
        body += "<td style=' text-align:left ; color: white;  background :mediumseagreen' > Pass Count </th>"
        body += "<td style=' text-align:left ; color: white;  background :mediumseagreen' > " + str(len([ key for key,value in scenarios.iteritems() if 'status' in value.keys() and value['status'] =="Passed"])) + " </th>"
        body += "</tr>"
        body += "<tr>"
        body += "<td style='  text-align:left ; color: white;  background :indianred' > Fail Count </th>"
        body += "<td style='  text-align:left ; color: white;  background :indianred' > " + str(len([ key for key,value in scenarios.iteritems() if 'status' in value.keys() and value['status'] =="Failed"]))+ " </th>"
        body += "</tr>"
        body += "<tr>"
        body += "<td style='  text-align:left ; color: black; background :#D3D3D3' > Total Count </th>"
        body += "<td style='  text-align:left ; color: black; background :#D3D3D3' > " + str(len(feature["scenarios"]))+ " </th>"
        body += "</tr>"
        body += "</table><br/><br/>"
        return body

    def build_latency_info (self,scenario):
        
        user_scenario = scenario["users"]["Ellie"]
        latency = None
        if ("latency" in user_scenario.keys()) :
            latency = user_scenario['latency']
        firmware_launch_time = 0
        if ("firmware_launch_time" in user_scenario.keys()):
            firmware_launch_time = user_scenario['firmware_launch_time']
        message=""
        message += "<table width='40%' cellspacing='5px' cellpadding='5px' style='font-family : Trebuchet MS'>"
        if (latency is not None and len(latency) > 0):
            for key,value in latency.iteritems():
                message += "<tr>"
                message += "<td style=' text-align:left ; color:black; text-color: black;' >"+ key+"</td>"
                message += "<td style=' text-align:left ; color:black; text-color: black;' >"+ str("{0:.2f}".format(np.mean(value))  if isinstance(value,list) else value)+"</td>"
                message += "</tr>"
        if (firmware_launch_time > 0):
            value = user_scenario["firmware_launch_time"]
            message += "<tr>"
            message += "<td style=' text-align:left ; color:black; text-color: black; ' >"+ "Firmware Launch Time"+"</td>"
            message += "<td style=' text-align:left ; color:black; text-color: black; ' >"+ str("{0:.2f}".format(np.mean(value))  if isinstance(value,list) else value)+"</td>"
            message += "</tr>"
        message += "</table>"
        return message

    def build_cpumem_info(self,scenario):
        user_scenario = scenario["users"]["Ellie"]
        message=""
        message += "<table width='40%' cellspacing='5px' cellpadding='5px' style='font-family : Trebuchet MS'>"
        if ("cpu_max" in user_scenario.keys()) :
            message += "<tr>"
            message += "<td style=' text-align:left ; color:black;text-color:black; ' >"+ "CPU MAX "+"</td>"
            value = user_scenario["cpu_max"]
            message += "<td style=' text-align:left ; color:black;text-color:black; ' >"+ str("{0:.2f}".format(np.mean(value))  if isinstance(value,list) else value) +"&#37;</td>"
            message += "</tr>"
        if ("cpu_avg" in user_scenario.keys()) :
            message += "<tr>"
            message += "<td style=' text-align:left ; color:black;text-color:black; ' >"+ "CPU AVG "+"</td>"
            value = user_scenario["cpu_avg"]
            message += "<td style=' text-align:left ; color:black;text-color:black; ' >"+ str("{0:.2f}".format(np.mean(value))  if isinstance(value,list) else value) +"&#37;</td>"
            message += "</tr>"
        if ("cpu_trimmed_avg" in user_scenario.keys()) :
            message += "<tr>"
            message += "<td style=' text-align:left ; color:black;text-color:black; ' >"+ "CPU TRIMMED AVG "+"</td>"
            value = user_scenario["cpu_trimmed_avg"]
            message += "<td style=' text-align:left ; color:black;text-color:black; ' >"+ str("{0:.2f}".format(np.mean(value))  if isinstance(value,list) else value) +"&#37;</td>"
            message += "</tr>"
        if ("mem_max" in user_scenario.keys()) :
            message += "<tr>"
            message += "<td style=' text-align:left ; color:black;text-color:black; ' >"+ "MEM MAX "+"</td>"
            value = user_scenario["mem_max"]
            message += "<td style=' text-align:left ; color:black;text-color:black; ' >"+ str("{0:.2f}".format(np.mean(value)) if isinstance(value,list) else value) +"MB</td>"
            message += "</tr>"
        if ("mem_avg" in user_scenario.keys()) :
            message += "<tr>"
            message += "<td style=' text-align:left ; color:black;text-color:black; ' >"+ "MEM TRIMMED AVG "+"</td>"
            value = user_scenario["mem_avg"]
            message += "<td style=' text-align:left ; color:black;text-color:black; ' >"+ str("{0:.2f}".format(np.mean(value))  if isinstance(value,list) else value) +"MB</td>"
            message += "</tr>"
        if ("mem_trimmed_avg" in user_scenario.keys()) :
            message += "<tr>"
            message += "<td style=' text-align:left ; color:black;text-color:black; ' >"+ "MEM AVG "+"</td>"
            value = user_scenario["mem_trimmed_avg"]
            message += "<td style=' text-align:left ; color:black;text-color:black; ' >"+ str("{0:.2f}".format(np.mean(value))  if isinstance(value,list) else value) +"MB</td>"
            message += "</tr>"
        message += "</table>"
        return message

    def build_scenario_html(self,scenarios):
        body = ""
        body += "<h2>Testcase Results:</h2>"
        body += "<table width='80%' cellspacing='5px' cellpadding='5px' style='font-family : Trebuchet MS'>"
        body += "<tr>"
        body += "<th style=' padding: 5px; text-align:left ; text-color: white; background :black' > Test Name </th>"
        body += "<th style=' padding: 5px; text-align:left ; text-color: white; background :black' > Status </th>"
        body += "<th style=' padding: 5px; text-align:left ; text-color: white; background :black' > Latency </th>"
        body += "<th style=' padding: 5px; text-align:left ; text-color: white; background :black' > CPU/MEM </th>"
        body += "</tr>"
        for key in scenarios.keys():
            body += "<tr>"
            body += "<td style='padding: 5px; text-align:left; background:linen' >" + key + "</td>"
            if (scenarios[key]['status'] == 'Passed'):
                body += "<td style=' padding: 5px; text-align:left ; color: white; background:mediumseagreen'>" + scenarios[key]['status'] + "</td>"
            else:
                failure_reason_string = "Failure Reason : Test Failure <br/>"
                for reason in scenarios[key]["failure_reason"]:
                    failure_reason_string += "Failure Reason : " + reason +"<br/>"
                body += "<td style='padding: 5px; text-align:left ; color: white; background:indianred'>" +  scenarios[key]['status'] + "<br/> "+failure_reason_string+"</td>"
                

            body += "<td style='padding: 5px; text-align:left; background:linen' >" + self.build_latency_info(scenarios[key]) + "</td>"
            body += "<td style='padding: 5px; text-align:left; background:linen' >" + self.build_cpumem_info(scenarios[key]) + "</td>"            

            body += "</tr>"
        body += "</table>"
        return body 

    def send_email(self, feature):

        try : 
            sg = sendgrid.SendGridAPIClient(apikey=self.sendgrid_api_key)
            from_email = Email("3pipautomation@domain.com")
            to_email = Email("dummy@domain.com")
            subject =  self.primary_test_device + " - Sakurai Automation "+ feature["name"] +" - " + feature["status"]
            
            content = self.build_email(feature)
            content = Content("text/html",content)
            mail = Mail(from_email, subject, to_email, content)
            personalization = Personalization()
            to_addresses = self.mail_to_users.split(",")
            for address in to_addresses :
                personalization.add_to(Email(address,address))
            mail.add_personalization(personalization)
            result =  mail.get()
            response = sg.client.mail.send.post(request_body=result)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print "Exception  : " + str(e)
            raise Exception(e)

