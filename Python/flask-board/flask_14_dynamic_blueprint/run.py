from flaskapp import create_app

app = create_app()

# sets the debug mode to True,
# to make sure server applies change actively
if __name__ == '__main__':
	app.run(debug=True)