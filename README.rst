Documentation
=============

Help:
====

Step 1:

$ Clone zopper.ws using git command:

$ git clone git@github.com/itssafi/zopper.ws

$ cd zopper.ws

Step 2:

Install setup.py using python 2.6.x

$ python setup.py install

$ python setup.py develop

Step 3:

Add 'REST client' add-ons in firefox browser

Step 4:

Start Server using below command

$ pserve development.ini --reload

Step 5:

Load data in database

url: http:172.0.0.1:8080/dataload/

method: POST

content-type: application/json

Payload should be in below format--

{"fields":[{"id":"a","label":"IMAGE INTENSIFICATION BASED DEVICES","type":"string"},{"id":"b","label":null,"type":"string"},{"id":"c","label":null,"type":"string"},{"id":"d","label":null,"type":"string"}],"data":[["DEVICE NAME","MGNIFICATION (X)","FIELD OF VIEW(degree)","RANGE(m)"],["Integrated Observation Equipment",7,7,2000],["Passive Night Vision Binocular (Mk-I)",4,10,500],["Passive Night Vision Goggles",1,40,225],["Passive Night Sight for 84 mm Carl",4,10,500],["Passive Night Sight for 5.56 mm Rifle",4,10,200],["Passive Night Sight for 5.56 mm LMG",4,10,200],["Passive Night Sight RCL Mk I",5,10,600],["Passive Night Sight RCL Mk II",6,9,600],["Driver Sight for T-55",1,40,100],["Gunners Night Sight for T-55",7,7,">800"],["Balloon Lifted Imaging & Surveillance","NA",2.1,4000],["Goggles for Aireforce",1,40,250],["Sight for 84 Mm",5.5,8,700]]}

Step 6:

Search data using given below url--

method: GET

Valid URL
---------
url: http:172.0.0.1:8080/searchdata/?filter=field_of_view=11,mgnification=8,range=800

http:172.0.0.1:8080/searchdata/?filter=field_of_view=11,mgnification=8

http:172.0.0.1:8080/searchdata/?filter=field_of_view=11

Invalid URL
-----------
url: http:172.0.0.1:8080/searchdata/?field_of_view=11,mgnification=8,range=800
