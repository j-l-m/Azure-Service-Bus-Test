from azure.servicebus import ServiceBusService, Message, Queue
from azure.storage.table import TableService, Entity
from azure.storage.queue import QueueService
import multiprocessing
import json
import uuid
import time

#script run by the receiver vms in the vm scale set
#stores successful requests to a table called 'req'
#stores failures to a table called 'fail'
#in order to monitor failures I also stored them to a storage queue
#by using the storage queue I could simply get query the queue for queue length with another script


def rec_messages(process_name):

	#create service bus service object
	bus_service = ServiceBusService(
		service_namespace='jlm4dde996c8a5680751',
		shared_access_key_name='RootManageSharedAccessKey',
		shared_access_key_value='ZPvfBo7KrZAf5zG+gs1MS4kSvCbcI4/uSfDDd/+rF3c=')

	#storage account credentials
	store_account_name = 'jlm4dde996c8a5680751'
	store_account_key  = 'SarGXuo2SGJEk2GpKWH1a3vBG9H0d+V0/y6BxYCfy/8GSCa1IAl18SX7VgBW6dVQxGwqJXHpQfDZ3amADYdqwA=='

	#create storage table service object
	table_service = TableService(
		account_name = store_account_name, 
		account_key = store_account_key)

	#create storage queue service object
	queue_service = QueueService(
		account_name = store_account_name, 
		account_key = store_account_key)

	#generate a uuid for the process.
	#this uuid is used as the partition key
	proc_id = str(uuid.uuid1())

	print("running...")
	
	while 1:
		try:
			#receive message, timeout after 15 seconds
			msg = bus_service.receive_queue_message('jlmtestqueue1', peek_lock = False, timeout = 15)
			
			#if timeout or there are no message on queue then msg.body is None
			if msg.body is not None:
				#if failure message store to 'fail' table and store a message on storage queue
				if msg.body.decode('utf-8') == 'Error Message':
					t = int(round(time.time() * 1000))
					j = {
						"PartitionKey": proc_id,
						"RowKey": "T%d" % (t,),
						"data" : "Error"
					}
					table_service.insert_entity('fail', j)
					queue_service.put_message('jlmtestregqueue1', u'Error Message')
				
				else:			
					j = msg.body
					j = json.loads(j)
					t = int(round(time.time() * 1000))
					ent ={
						"PartitionKey"		: proc_id,
						"RowKey"			: "T%d" % (t,),
						"TransactionID"		: j["TransactionID"],
						"UserID"			: j["UserId"],
						"SellerID"			: j["SellerID"],
						"ProductName"		: j["Product Name"],
						"SalePrice"			: j["Sale Price"],
						"TransactionDate"	: j["Transaction Date"]
					}
					table_service.insert_entity('req', ent)
					print(j["Sale Price"])
		except Exception as e:
			s = str(e)
			print(s)




#main program
if __name__ == '__main__':
	p = multiprocessing.Pool(7)
	params = []
	for i in range(7):
		params.append("%s: %s" % ("Process", i))
	#try:
	p.map(rec_messages, params)
	print("hi...")

	while 1:
		pass
	#except:
		#print("stopped")
		#p.terminate()
