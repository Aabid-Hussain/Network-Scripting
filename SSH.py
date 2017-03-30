import paramiko

# To open SSH client
ssh = paramiko.SSHClient()
#adding policies to connection, if it is not defined code will through error while connecting device.
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect('192.168.1.20', port=22,username='admin', password='aabid')

stdin, stdout, stderr = ssh.exec_command("show ip route")

output = stdout.readlines()

print '\n'.join(output)



