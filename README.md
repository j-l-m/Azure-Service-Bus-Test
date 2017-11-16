## Pre-requisites:

1. A resource group containing the service bus and storage account must already be set up
2. The service bus must already have a queue called **jlmtestqueue1**
3. The storage account must have:
	- A queue called **jlmtestregqueue1"
	- A table called **req**
	- A table called **fail**
4. If the service bus or storage account names/keys have changed then they will have to be changed in the python scripts as well.
5. Python 3.6 is required as well as the azure SDK for python.
	- pip install azure

## Deploying
When deploying the template, the following two fields must be changed in the Settings section of the deployment screen in Azure portal
- **service_bus_name**   this is the name or namespace for the service bus
- **resgrp_name_for_bus_and_storage**   this is the name of the resource group containing the service bus and storage account

The template deploys the VM Scale Set that will receive messages from the service bus queue and store them in the storage account.


## Steps
1. Download the following files and place them in the same folder:
	- **monitor.py**
	- **send_msgs.py**
	- **send_msgs.bat**

2. **monitor.py** - This script polls the service bus queue and storage queue for a message count.
	- It is used to monitor the service bus and the number of failures stored
	- Failures are stored to table storage but also to a storage queue as it is easy to get count from a storage queue.

3. Send messages by running **send_msgs.bat**
	- This .bat file will run 10 instances of **send_msgs.py**
	- This was necessary to get the required output. 
	- Multiprocessing was used but the code seems to be bound by the network operation of sending messages. This resulted in poor CPU utilisation and slow message sending.
	- Monitor the message count of the service bus with either the monitor.py script or use the metrics on the azure portal
	- Use Ctrl+C to close the terminals when the 600 000 messages are generated.
	- **NOTE:** Close each terminal individually with Ctrl+C and wait for the processes to end. Closing the window early can cause the processes to hang or remain running in the background.

4. Deploy the template. Follow the instructions for deploying described above.

5. You can monitor the consumption of messages in the monitor.py terminal, here you will see the number of failure messages stored. Additionally you can use the overview on azure portal for the resource.



<a href="https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fj-l-m%2Ftestrepo%2Fmaster%2Fjlm_a3_comp6905_template.json" target="_blank">
    <img src="http://azuredeploy.net/deploybutton.png"/>
</a>
