from flask import Flask

app = Flask (__name__)
app.config ['SECRET_KEY'] = 'edb55e2007638dae6bde011b7ff4686f'

from application import routes
