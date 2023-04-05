from flask import Flask, request
from flask_smorest import Api
from flask_cors import CORS

from routes.email.email import email_blueprint

from dotenv import find_dotenv, dotenv_values

config = dotenv_values(dotenv_path=find_dotenv())

app = Flask(__name__)

# TODO: Move configurations to Config class
app.config["API_TITLE"] = "Personal API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)
CORS(app, origins=config["CORS_ORIGINS"])

api.register_blueprint(email_blueprint)


# log request and response
@app.after_request
def log_request_and_response(response):
    request_bound = f"##########################-REQUEST-###########################"
    response_bound = f"##########################-RESPONSE-##########################"
    end_bound = f"##########################-END-###############################"
    # log request
    if request.method == "GET":
        app.logger.info(request_bound)
        app.logger.info(f"method: {request.method}")
        app.logger.info(f"url: {request.url}")
        app.logger.info(f"args: {request.args.__dict__}")
    if request.method == "POST":
        app.logger.info(request_bound)
        app.logger.info(f"method: {request.method}")
        app.logger.info(f"url: {request.url}")
        app.logger.info(f"json: {request.json}")

    # log response
    app.logger.info(response_bound)
    app.logger.info(f"status: {response.status}")
    app.logger.info(f"json: {response.json}")
    app.logger.info(end_bound)

    return response


@app.route("/")
def health_check():
    return {"status": "OK", "message": "Personal API is up and running"}


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
    pass
