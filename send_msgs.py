from azure.servicebus import ServiceBusService, Message, Queue
import multiprocessing
import datetime
import json
#import sys

#script starts 7 processes to send messages to populate service bus queue
#run from local machine
#script is bound on the network operation of sending the messages, therefore output is slow
#to remedy the above issue I included a .bat file to run 6 instances of this script which should work


def send_messages(process_name):
	
	#create service bus service object
	bus_service = ServiceBusService(
    service_namespace='jlm4dde996c8a5680751',
    shared_access_key_name='RootManageSharedAccessKey',
    shared_access_key_value='ZPvfBo7KrZAf5zG+gs1MS4kSvCbcI4/uSfDDd/+rF3c=')
	print("running...")

	#create message dictionary
	msgobj = {
		"TransactionID": "1",
		"UserId":"A1",
		"SellerID":"S1",
		"Product Name":"Financial Trap",
		"Sale Price":1000000,
		"Transaction Date": datetime.date.today().strftime("%B %d, %Y")
	}

	#convert message dictionary to json string
	msg_json = json.dumps(msgobj)

	count = 0
	while 1:
		try:
			#create and send failure message after every 1000 messages
			if count == 1000:
				msg = Message('Error Message')
				bus_service.send_queue_message('jlmtestqueue1', msg)
				count = 0
			#send the json string as a message
			else:
				msg = Message(msg_json)
				bus_service.send_queue_message('jlmtestqueue1', msg)
				count += 1
	
		except KeyboardInterrupt:
			print("failure")
			return ("X")




#main program
if __name__ == '__main__':

	#create process pool
	p = multiprocessing.Pool(7)
	params = []
	#populate an array with process names as parameters
	for i in range(7):
		params.append("%s: %s" % ("Process", i))
	
	y = "hi"
	#map and start processes
	try:
		y= p.map(send_messages, params)
		print(y)

	except KeyboardInterrupt:
		print(y)
		print("ended")	

	#while 1:
		#pass
	
