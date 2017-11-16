from azure.storage.queue import QueueService
from azure.servicebus import ServiceBusService, Message, Queue
import time
import sys


def monitor_failures():

	bus_service = ServiceBusService(
		service_namespace='jlm4dde996c8a5680751',
		shared_access_key_name='RootManageSharedAccessKey',
		shared_access_key_value='ZPvfBo7KrZAf5zG+gs1MS4kSvCbcI4/uSfDDd/+rF3c=')

	store_account_name = 'jlm4dde996c8a5680751'
	store_account_key  = 'SarGXuo2SGJEk2GpKWH1a3vBG9H0d+V0/y6BxYCfy/8GSCa1IAl18SX7VgBW6dVQxGwqJXHpQfDZ3amADYdqwA=='

	queue_service = QueueService(
		account_name = store_account_name, 
		account_key = store_account_key)


	queue_name = 'jlmtestregqueue1'
	sys.stdout.write("\n")


	try:
		while 1:
			metadata = queue_service.get_queue_metadata(queue_name)
			count = metadata.approximate_message_count
			sbq_count = bus_service.get_queue('jlmtestqueue1').message_count
			t = time.strftime("%H:%M:%S")
			output = "Messages on Service bus: %d\tFailures stored: %d   Time: %s" % (sbq_count, count, t)
			sys.stdout.write(output + "\r")
			sys.stdout.flush()
			time.sleep(10)

	except KeyboardInterrupt:
			print('\nKeyboard Interrupt')

monitor_failures()
