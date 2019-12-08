from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class Car(Base):
    __tablename__ = 'car'
   
    id = Column(Integer, primary_key=True)
    image = Column(String(250))
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
       }
 
class CarType(Base):
    __tablename__ = 'car_type'


    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))    
    car_id = Column(Integer,ForeignKey('car.id'))
    car = relationship(Car)


    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.model,
           'description'         : self.description,
           'id'         : self.id,
           'price'         : self.price,
           
       }



engine = create_engine('sqlite:///cars.db')
 

Base.metadata.create_all(engine)

