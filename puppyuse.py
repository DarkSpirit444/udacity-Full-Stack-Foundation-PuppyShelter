import datetime
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# 1. Query all of the puppies and return the results in ascending alphabetical order
puppies = session.query(Puppy).order_by(Puppy.name).all()
for puppy in puppies:
	print puppy.name

# 2. Query all of the puppies that are less than 6 months old organized by the youngest first
six_months = datetime.date.today() - datetime.timedelta(6*365/12)
puppies = session.query(Puppy).filter(Puppy.dateOfBirth >= str(six_months)).order_by(Puppy.dateOfBirth.desc())
for puppy in puppies:
	print "%s %s" % (puppy.name, puppy.dateOfBirth)

# 3. Query all puppies by ascending weight
puppies = session.query(Puppy).order_by(Puppy.weight)
for puppy in puppies:
	print "%s %s" % (puppy.name, puppy.weight)

#4. Query all puppies group by the shelter in which they are staying
puppiesshelters = session.query(Puppy, Shelter).join(Shelter).order_by(Puppy.shelter_id)
for (puppy,shelter) in puppiesshelters:
	print "%s %s" % (puppy.name, shelter.name)

#5. Query number of puppies group by the shelter in which they are staying
puppiesshelters = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Puppy.shelter_id)
for (shelter,count) in puppiesshelters:
	print "%s %s" % (shelter.name, count)

def register_puppy(name, gender, dateOfBirth, weight, shelter_id):
	shelter = session.query(Shelter).filter(Shelter.id == shelter_id).one()
	print "%s %s" % (shelter.maximum_capacity, shelter.current_occupancy)
	if shelter.current_occupancy < shelter.maximum_capacity:
		new_puppy = Puppy(name = name, gender = gender, dateOfBirth = dateOfBirth, shelter_id = shelter_id, weight = weight)
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

def adopt_puppy(puppy_id, adopter_ids):
	puppy = session.query(Puppy).filter(Puppy.id == puppy_id).one()
	shelter = session.query(Shelter).join(Puppy).filter(Puppy.id == puppy_id).one()
	if shelter.current_occupancy > 0 and not puppy.adopter_ids:
		shelter.current_occupancy = shelter.current_occupancy - 1
		puppy.adopter_ids = adopter_ids
		session.add(puppy)
		session.add(shelter)
		session.commit()
	else:
		print "Error!  Puppy %s has already been adopted!" % puppy.name


#register_puppy("Isaac", "male", datetime.date.today(), 10.0, 3)
#register_puppy("Rachael", "female", datetime.date.today(), 10.0, 3)

#puppiesshelters = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Puppy.shelter_id)
#for (shelter,count) in puppiesshelters:
	#print "%s %s" % (shelter.name, count)
adopt_puppy(14, [4, 2, 5])