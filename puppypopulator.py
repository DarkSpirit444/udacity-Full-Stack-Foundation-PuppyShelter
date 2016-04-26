from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from puppies import Base, Shelter, Puppy
#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random


engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()


#Add Shelters
shelter1 = Shelter(name = "Oakland Animal Services", address = "1101 29th Ave", city = "Oakland", state = "California", zipCode = "94601", maximum_capacity = 30, website = "oaklandanimalservices.org")
session.add(shelter1)

shelter2 = Shelter(name = "San Francisco SPCA Mission Adoption Center", address="250 Florida St", city="San Francisco", state="California", zipCode = "94103", maximum_capacity = 20, website = "sfspca.org")
session.add(shelter2)

shelter3 = Shelter(name = "Wonder Dog Rescue", address= "2926 16th Street", city = "San Francisco", state = "California" , zipCode = "94103", maximum_capacity = 25, website = "http://wonderdogrescue.org")
session.add(shelter3)

shelter4 = Shelter(name = "Humane Society of Alameda", address = "PO Box 1571" ,city = "Alameda" ,state = "California", zipCode = "94501", maximum_capacity = 25, website = "hsalameda.org")
session.add(shelter4)

shelter5 = Shelter(name = "Palo Alto Humane Society" ,address = "1149 Chestnut St." ,city = "Menlo Park", state = "California" ,zipCode = "94025", maximum_capacity = 15, website = "paloaltohumane.org")
session.add(shelter5)

session.commit()

#Add Puppies

male_names = ["Bailey", "Max", "Charlie", "Buddy","Rocky","Jake", "Jack", "Toby", "Cody", "Buster", "Duke", "Cooper", "Riley", "Harley", "Bear", "Tucker", "Murphy", "Lucky", "Oliver", "Sam", "Oscar", "Teddy", "Winston", "Sammy", "Rusty", "Shadow", "Gizmo", "Bentley", "Zeus", "Jackson", "Baxter", "Bandit", "Gus", "Samson", "Milo", "Rudy", "Louie", "Hunter", "Casey", "Rocco", "Sparky", "Joey", "Bruno", "Beau", "Dakota", "Maximus", "Romeo", "Boomer", "Luke", "Henry"]

female_names = ['Bella', 'Lucy', 'Molly', 'Daisy', 'Maggie', 'Sophie', 'Sadie', 'Chloe', 'Bailey', 'Lola', 'Zoe', 'Abby', 'Ginger', 'Roxy', 'Gracie', 'Coco', 'Sasha', 'Lily', 'Angel', 'Princess','Emma', 'Annie', 'Rosie', 'Ruby', 'Lady', 'Missy', 'Lilly', 'Mia', 'Katie', 'Zoey', 'Madison', 'Stella', 'Penny', 'Belle', 'Casey', 'Samantha', 'Holly', 'Lexi', 'Lulu', 'Brandy', 'Jasmine', 'Shelby', 'Sandy', 'Roxie', 'Pepper', 'Heidi', 'Luna', 'Dixie', 'Honey', 'Dakota']

puppy_images = ["http://pixabay.com/get/da0c8c7e4aa09ba3a353/1433170694/dog-785193_1280.jpg?direct", "http://pixabay.com/get/6540c0052781e8d21783/1433170742/dog-280332_1280.jpg?direct","http://pixabay.com/get/8f62ce526ed56cd16e57/1433170768/pug-690566_1280.jpg?direct","http://pixabay.com/get/be6ebb661e44f929e04e/1433170798/pet-423398_1280.jpg?direct","http://pixabay.com/static/uploads/photo/2010/12/13/10/20/beagle-puppy-2681_640.jpg","http://pixabay.com/get/4b1799cb4e3f03684b69/1433170894/dog-589002_1280.jpg?direct","http://pixabay.com/get/3157a0395f9959b7a000/1433170921/puppy-384647_1280.jpg?direct","http://pixabay.com/get/2a11ff73f38324166ac6/1433170950/puppy-742620_1280.jpg?direct","http://pixabay.com/get/7dcd78e779f8110ca876/1433170979/dog-710013_1280.jpg?direct","http://pixabay.com/get/31d494632fa1c64a7225/1433171005/dog-668940_1280.jpg?direct"]

#This method will make a random age for each puppy between 0-18 months(approx.) old from the day the algorithm was run.
def CreateRandomAge():
	today = datetime.date.today()
	days_old = randint(0,540)
	birthday = today - datetime.timedelta(days = days_old)
	return birthday

#This method will create a random weight between 1.0-40.0 pounds (or whatever unit of measure you prefer)
def CreateRandomWeight():
	return random.uniform(1.0, 40.0)

def PopulatePuppies(list, gender):
	for i,x in enumerate(list):
		#shelter_id=randint(1,5)
		shelter_id = find_vacancy()

		register_puppy(name = x, gender = gender, dateOfBirth = CreateRandomAge(), weight= CreateRandomWeight(), picture=random.choice(puppy_images), shelter_id=shelter_id)
		#shelter = session.query(Shelter).filter_by(id = shelter_id).one()
		#shelter.current_occupancy = shelter.current_occupancy + 1
		#session.add(shelter)
		#new_puppy = Puppy(name = x, gender = gender, dateOfBirth = CreateRandomAge(),picture=random.choice(puppy_images) ,shelter_id=shelter_id, weight= CreateRandomWeight())
		#session.add(new_puppy)
		#session.commit()

def register_puppy(name, gender, dateOfBirth, weight, picture, shelter_id):
	shelter = session.query(Shelter).filter(Shelter.id == shelter_id).one()
	if shelter.current_occupancy < shelter.maximum_capacity:
		new_puppy = Puppy(name = name, gender = gender, dateOfBirth = dateOfBirth, shelter_id = shelter_id, picture = picture, weight = weight)
		add_puppy(new_puppy, shelter)
	else:
		alternative_shelter = find_vacancy()
		if alternative_shelter == 0:
			print "All Shelters are full!!!"
		else:
			print "Re-routing puppy from Shelter %s to %s" % (shelter_id, alternative_shelter)
			shelter = session.query(Shelter).filter(Shelter.id == alternative_shelter).one()
			new_puppy = Puppy(name = name, gender = gender, dateOfBirth = dateOfBirth, shelter_id = alternative_shelter, weight = weight)
			add_puppy(new_puppy, shelter)

def find_vacancy():
	shelter = session.query(Shelter).order_by((Shelter.maximum_capacity - Shelter.current_occupancy).desc()).all()
	if not shelter or shelter[0].current_occupancy >= shelter[0].maximum_capacity:
		# no more vacancies
		return 0
	else:
		return shelter[0].id

def add_puppy(puppy, shelter):
	shelter.current_occupancy = shelter.current_occupancy + 1
	session.add(shelter)
	session.add(puppy)
	session.commit()

PopulatePuppies(male_names, "male")
PopulatePuppies(female_names, "female")