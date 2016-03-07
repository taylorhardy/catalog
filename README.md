Problem: You will develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

Design frameworks: Bootstrap, Flask, Github-Flask, SQLAlchemy

Database Used: SQLite

How to run: First install the frameworks, other than bootstrap where a CDN was used. Then the database needs to be setup, so in your python CLI use 'python database_setup.py', this will create the schema. Then you can add predefined data to the database using 'python addData.py'. After there is data in the database start the application with 'python application.py'