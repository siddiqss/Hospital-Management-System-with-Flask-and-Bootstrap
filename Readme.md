# Health Monitoring System with Flask and Bootstrap (bootswatch theme)
An automated appointment booking system for hospitals where a 
patient's appointment is booked automatically depending on 
patient's body temperature and pulse rate.
This system gets patient's body temperature, pulse rate and
location from ThingSpeak which is integrated with IoT system
consisting of IR temperature sensor, pulse rate sensor and
GPS.
###### This system is integrated with ThingSpeak 

## Specs
This system is built in flask and flask-bootstrap and sqlite is 
used as database

## How to use:
* Create a virtual environment. You can learn how to create 
a [virtual environment from here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
* After activating virtual environment, run 
```
pip install -r requirements.txt
```

## Integrate ThingSpeak
You need to create an account on ThingSpeak and use API keys.
Puts API keys in backend/read_data.py 

## How to solve db errors:
To remove all data from database, run python in virtual environment

```
from backend import db
db.drop_all()
exit()
```
Now run these commands to initialize database:
```
flask db init
flask db migrate -m "DB initiated"
flask db upgrade
```
