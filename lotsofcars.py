from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Car, Base, CarType
 
engine = create_engine('sqlite:///cars.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



#Menu for BMW
car1 = Car(name = "BMW", image = "/static/bmw.jpg")

session.add(car1)
session.commit()


menuItem1 = CarType(name = "M340i Sedan", description = "Model Year: 2020,State: New ,color: black, CC: 3500, available", price = "$180.000", car = car1)

session.add(menuItem1)
session.commit()

menuItem2 = CarType(name = "M240i Coupe", description = "Model Year: 2017,State: Used ,color: black, CC: 2500, available", price = "$40.000", car = car1)

session.add(menuItem2)
session.commit()

menuItem3 = CarType(name = "M550i xDrive Sedan", description = "Model Year: 2019,State: New ,color: black, CC: 2500, available",price = "$51.000", car = car1)

session.add(menuItem3)
session.commit()





#Menu for Super Stir Ferrari
car2 = Car(name = "Ferrari", image = "/static/ferrari.jpg")

session.add(car2)
session.commit()


carType1 = CarType(name = "488 Pista", description = "Model Year: 2020,State: New ,color: gold, CC: 6500, only 1 piece available, for offer call : 01113722390", price = "$3.350.000", car = car2)

session.add(carType1)
session.commit()

carType2 = CarType(name = "GTC4Lusso", description = "Model Year: 2019,State: New ,color: red, CC: 3000, available", price = "$120.000", car = car2)

session.add(carType2)
session.commit()

carType3 = CarType(name = "Portofino", description = "Model Year: 2020,State: New ,color: green, CC: 2000, available", price = "$80.000" ,car = car2)

session.add(carType3)
session.commit()






#Menu for Panda Audi
car3 = Car(name = "Audi", image = "/static/audi.png")

session.add(car3)
session.commit()


carType1 = CarType(name = "RS5 Sportback", description = "Model Year: 2020,State: New ,color: black, CC: 2500, available", price = "$70.200", car = car3)

session.add(carType1)
session.commit()

carType2 = CarType(name = "Audi Q3", description = "Model Year: 2020,State: New ,color: black, CC: 2000, available", price = "$50.800", car = car3)

session.add(carType2)
session.commit()

carType3 = CarType(name = "Audi R8", description = "Model Year: 2019,State: New ,color: white, CC: 2000, available after 1 week", price = "$40.720", car = car3)

session.add(carType3)
session.commit()



#Menu for Ford
car4 = Car(name = "Ford", image = "/static/ford.jpg")

session.add(car4)
session.commit()


carType1 = CarType(name = "Ford Mustang", description = "Model Year: 2020,State: New ,color: green, CC: 2000 available", price = "$51.000", car = car4)

session.add(carType1)
session.commit()

carType2 = CarType(name = "Ford Fiesta", description = "Model Year: 2020,State: New ,color: blue, CC: 1600, available", price = "$45.000", car = car4)

session.add(carType2)
session.commit()

carType3 = CarType(name = "Ford Falcon", description = "Model Year: 2020,State: New ,color: orange, CC: 1300, available soon call us on 01113722390", price = "$38.000", car = car4)

session.add(carType3)
session.commit()




#Menu for Cadillac
car5 = Car(name = "Cadillac", image = "/static/cadillac.jpg")

session.add(car5)
session.commit()


carType1 = CarType(name = "Cadillac CTS", description = "Model Year: 2020,State: New ,color: white, CC: 2000, available", price = "$50.100", car = car5)

session.add(carType1)
session.commit()

carType2 = CarType(name = "Cadillac XT4", description = "Model Year: 2017,State: used ,color: blue, CC: 1500, available", price = "$15.200",  car = car5)

session.add(carType2)
session.commit()

carType3 = CarType(name = "Cadillac XT5", description = "Model Year: 2020,State: New ,color: red, CC: 1800, available after 2 weeks ", price = "$38.390", car = car5)

session.add(carType3)
session.commit()






#Menu for Mercedes 
car6 = Car(name = "Mercedes", image = "/static/mercedes.jpg")

session.add(car6)
session.commit()


carType1 = CarType(name = "Mercedes-Benz E-Class", description = "Model Year: 2020,State: New ,color: red, CC: 2800",  price = "$58,900", car = car6)

session.add(carType1)
session.commit()

carType2 = CarType(name = "Mercedes-Benz C-Class", description = "Model Year: 2020,State: used ,color: red, CC: 2000",  price = "$41,400",  car = car6)

session.add(carType2)
session.commit()

carType3 = CarType(name = "Mercedes-Benz GLA", description = "Model Year: 2020,State: New ,color: red, CC: 2000",  price = "41,300",  car = car6)

session.add(carType3)
session.commit()






#Menu for Toyota
car7 = Car(name = "Toyota", image = "/static/toyta.jpg")

session.add(car7)
session.commit()


carType1 = CarType(name = "corolla", description = "Model Year: 2005, State: Used ,color: black, CC: 1300", price = "$35.000", car = car7 )

session.add(carType1)
session.commit()

carType2 = CarType(name = "yaris", description = "Model Year: 2020, State: New ,color: black, CC: 1600", price = "$32.000", car = car7)

session.add(carType2)
session.commit()

print "added menu items!"


