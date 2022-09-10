from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ftwretfr5wew87e67fgutrwt564g67t5yeg656'

from pay_flask import routes