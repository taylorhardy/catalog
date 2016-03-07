# got idea for github login from https://github.com/cenkalti/github-flask/blob/master/example.py
# github-flask login code from https://github-flask.readthedocs.org/en/latest/

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, g, session
app = Flask(__name__)


from flask.ext.github import GitHub

# config github login and app secret
app.config['GITHUB_CLIENT_ID'] = '6082ec605cd87c9c44ed'
app.config['GITHUB_CLIENT_SECRET'] = '2c96e4962140f731ce49789407a8f9953787984d'
github_callback_url = "http://localhost:5000/callback"
github = GitHub(app)
app_secret = 'SuperSecretKey'

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker,scoped_session
from database_setup import Base, Category, Item, User
engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine

db_session = scoped_session(sessionmaker(
	autocommit=False,
	autoflush=False,
	bind=engine))

Base.query = db_session.query_property()

# create routes


@app.route('/')
@app.route('/catalog')
# main view of site
def showCatalog():
	user = session.get('user_id', None)
	print("user", user)
	categories = Category.query.all()
	items = Item.query.order_by(Item.created.desc()).all()
	return render_template('catalog.html', categories=categories, items=items, user=user)


@app.route('/catalog/<string:category_name>/')
# route to view items by catalog
def showCategory(category_name):
	categories = Category.query.all()
	category = Category.query.filter_by(name=category_name).one()
	items = Item.query.filter_by(category = category).all()
	return render_template('catalog.html', categories=categories, items=items, category=category)


@app.route('/login')
# route to authorize login from github
def login():
	if session.get('user_id', None) is None:
		return github.authorize()
	else:
		return 'Already logged in'


@app.route('/callback')
@github.authorized_handler
# callback for github flask login
def authorized(oauth_token):
	next_url = request.args.get('next') or url_for('showCatalog')
	if oauth_token is None:
		# something went wrong
		flash("Authorization failed")
		flash(request.args.get('error'))
		flash(request.args.get('error_description'))
		flash(request.args.get('error_uri'))
		return redirect(next_url)
	user = User.query.filter_by(github_access_token=oauth_token).first()

	if user is None:
		# new user is not in database
		user = User(name="", github_access_token=oauth_token)
		db_session.add(user)
	# save oauth token in database
	user.github_access_token = oauth_token
	db_session.commit()
	session['user_id'] = user.id
	flash("User " + user.name + " logged in")
	return redirect(next_url)


@github.access_token_getter
# part of the github flask login
def token_getter():
	user = g.user
	if user is not None:
		return user.github_access_token


@app.route('/logout')
# logout route
def logout():
	session.pop('user_id', None)
	return redirect(url_for('showCatalog'))


@app.route('/item/<int:item_id>/')
# route to view items
def showItem(item_id):
	# assign user_id from the session to the user variable
	user = session.get('user_id', None)
	print("user", user)
	item = Item.query.filter_by(id=item_id).one()
	return render_template('item.html', item=item, user=user)


@app.route('/catalog/<string:category_name>/new', methods=['GET', 'POST'])
# route for adding new items
def newItem(category_name):
	categories = Category.query.all()
	category = Category.query.filter_by(name=category_name).one()
	user = session.get('user_id', None)
	# assign user_id from the session to the user variable
	if user is not None:
		# check to see if user is logged in
		if request.method == 'POST':
			# check if an item name was entered and asks for name if not
			if request.form['name'] != "":
				categoryName = Category.query.filter_by(name=request.form['category']).one()
				item = Item(
					name=request.form['name'],
					description=request.form['description'],
					category=categoryName)
				db_session.add(item)
				db_session.commit()
				flash("Item " + item.name + " added to " + item.category.name)
				return redirect(url_for('showCategory', category_name=categoryName.name))
			else:
				flash("Item name must be populated")
				return redirect(url_for('newItem', category_name=category_name))
		else:
			return render_template('newItem.html', category=category, categories=categories, user=user)
	else:
		flash("You must be logged in to add items")
		return redirect(url_for('showCatalog'))


@app.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
# route to edit items
def editItem(item_id):
	item = Item.query.filter_by(id=item_id).one()
	user = session.get('user_id', None)
	if user is not None:
		if request.method == 'POST':
			# check if an item name was entered
			if request.form['name'] != "":
				item.name = request.form['name']
				item.description = request.form['description']
				if request.form['category']:
					category = Category.query.filter_by(name=request.form['category']).one()
					item.category = category
				db_session.add(item)
				db_session.commit()
				flash("Item " + item.name + " added")
				return redirect(url_for('showItem', item_id=item.id, user=user))
			else:
				flash("Item name must be populated")
				return redirect(url_for('editItem', item_id=item.id, user=user))
		else:
			categories = Category.query.all()
			return render_template('editItem.html', item=item, categories=categories, user=user)
	else:
		flash("You must be logged in to edit items")
		return redirect(url_for('showCatalog'))


@app.route('/item/<int:item_id>/delete/', methods=['GET', 'POST'])
# route to delete item
def deleteItem(item_id):
	item = Item.query.filter_by(id=item_id).one()
	category = item.category
	user = session.get('user_id', None)
	if user is not None:
		if request.method == 'POST':
			flash("Item " + item.name + " deleted")
			db_session.delete(item)
			db_session.commit()
			return redirect(url_for('showCategory', category_name=category.name))
		else:
			return render_template('deleteItem.html', item=item, user=user)
	else:
		flash("You must be logged in to delete items")
		return redirect(url_for('showCatalog'))




@app.route('/json')
# route to display the json data from the database
def json():
	list = []
	items = Item.query.all()
	for item in items:
		list.append({
			"name": item.name,
			"id": item.id,
			"description": item.description,
			"category": item.category.name,
		})
	return jsonify({"items": list})

if __name__ == '__main__':
	app.debug = True
	app.secret_key = app_secret
	app.run(host='0.0.0.0', port=5000)
