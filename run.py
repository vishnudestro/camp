"""
run.py is the typical application server runner for flask.

Please note that this is only for a development server.
For production server, go for wsgi.py

"""

from camp import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=2000, host="0.0.0.0")
