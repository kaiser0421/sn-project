from flask import Flask
from flasgger import Swagger

from apis.api import user_api

app = Flask(__name__)
swagger = Swagger(app)

app.register_blueprint(user_api, url_prefix='/v1')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)