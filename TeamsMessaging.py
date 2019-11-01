import requests
   
class TeamsMessaging:
    def __init__(self, teams_webhooks):
        self.schedule_webhook = teams_webhooks["schedule_webhook"]
        self.success_webhook = teams_webhooks["success_webhook"]
        self.failure_webhook = teams_webhooks["failure_webhook"]
        self.info_webhook = teams_webhooks["info_webhook"]

    def send_schedule_message(self, message):
        headers = {
            'Content-Type': 'application/json'
        }
        # body = {
        #     "text":"<p style=\"color:amber;\"> Perf Test run on Trio scheduled by v-sigop </p>"
        # }
        body = {
            'text':'AUTO :' + '<p style=\"color:amber\">' + message +'</p>'
        }
        r = requests.post(self.schedule_webhook,headers=headers,json=body)
        print r.status_code
        print r.text

    def send_success_message(self, message):
        headers = {
            'Content-Type': 'application/json'
        }
        body = {
            'text':'AUTO :' + '<p style=\"color:green\">' + message +'</p>'
        }
        r = requests.post(self.success_webhook,headers=headers,json=body)
        print r.status_code
        print r.text

    def send_failure_message(self, message):
        headers = {
            'Content-Type': 'application/json'
        }
        body = {
            'text':'AUTO :' + '<p style=\"color:red\">' + message +'</p>'
        }
        r = requests.post(self.failure_webhook,headers=headers,json=body)
        print r.status_code
        print r.text

    def send_info_message (self, message):
        headers = {
            'Content-Type': 'application/json'
        }
        body = {
            'text':'AUTO :' + '<p style=\"color:black\">' + message +'</p>'
        }
        r = requests.post(self.info_webhook,headers=headers,json=body)
        print r.status_code
        print r.text