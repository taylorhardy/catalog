from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Category, Base, Item, User
 
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()

# add categories to the sqlite database

Basketball = Category(name="Basketball")
session.add(Basketball)

Baseball = Category(name="Baseball")
session.add(Baseball)

Snowboarding = Category(name="Snowboarding")
session.add(Snowboarding)

Soccer = Category(name="Soccer")
session.add(Soccer)

Golf = Category(name="Golf")
session.add(Golf)

IceHockey = Category(name="Ice Hockey")
session.add(IceHockey)

Googles = Item(name="Googles", category=Snowboarding)
session.add(Googles)

# add items and assign category and descriptions.

Bat = Item(
       name="Bat",
       category=Baseball)
session.add(Bat)

Driver = Item(
        name="Driver",
        category=Golf,
        description="Golf club for hitting long distances.")
session.add(Driver)

SoccerBall = Item(
        name="Ball",
        category=Soccer,
        description="Ball in which to play soccer with")
session.add(SoccerBall)

Snowboard = Item(
        name="Snowboard",
        category=Snowboarding,
        description="Board in which you can ride on the snow")
session.add(Snowboard)

HockeyStick = Item(
        name="Hockey Stick",
        category=IceHockey,
        description="The stick used to play Hockey with")
session.add(HockeyStick)

GolfBalls = Item(
        name="Golf Balls",
        category=Golf,
        description="Small white balls used to play golf with")
session.add(GolfBalls)

session.commit()

