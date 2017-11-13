from azure.servicebus import ServiceBusService, Message, Queue
from azure.storage.table import TableService, Entity
import multiprocessing
import json
import uuid
import time


def send_messages(nothinghere):
	bus_service = ServiceBusService(
	service_namespace='jlmtestservicebus1',
	shared_access_key_name='RootManageSharedAccessKey',
	shared_access_key_value='Bdlyngz0JiuScJjBoFEDBJiDTPNB9DCNZFj4cqm49D4=')

	table_service = TableService(
	account_name='jlmteststorage1', 
	account_key='f9LanXceS3/JujWIH9f6xKxhYmCUEf3XlwBeDUUSMBdvSZcpsII5/I+4VxpkbVtBhe1CW//lBoLBSGzpWfR9eQ==')

	proc_id = str(uuid.uuid1())
	print("running...")
	count = 0
	while 1:
		try:
			msg = bus_service.receive_queue_message('jlmtestqueue1', peek_lock = False, timeout = 20)
			if msg.body is not None:
				if msg.body.decode('utf-8') == 'Error Message':
					t = int(round(time.time() * 1000))
					j = {
						"PartitionKey": proc_id,
						"RowKey": "T%d" % (t,),
						"data" : "Error"
					}
					table_service.insert_entity('fail', j)
				
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
	p.map(send_messages, params)
	print("running...")

	while 1:
		pass
	#except:
		#print("stopped")
		#p.terminate()
