# time0ut-C2

eeeee
## Note


This is not completed at all... plan to add more features and hopefully cook up an agent


## Info

During the year 2 holiday (before going to year 3), I spent a bit of my time building a simple C2-server in python. It have many functionalities like getting information of the client machine and using the command prompt of the machine.

I am completely new to these kind of stuff therefore the C2-server should be quite bad (or just trash). I did it just for fun and as long as it works and acts like c2-server, I'm fine with it. However, after I gain more knowledge, I would like to really build a full scale c2-server where people will use it in the real world.


### c2-server.py
A basic server that I have created that have functions in them


### connect.py
This script is use to connect to c2-server.py locally


### old_trojan.py
This trojan acts like a task manager where it shows the user the usage of stuffs. 'blob' is old_maleware.py encoded in base64. There might be an issue where the connection does not persist


### old_malware.py
The malicious part of old_trojan.py where it attempts to connect to server
