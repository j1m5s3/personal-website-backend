import requests

from flask.views import MethodView, request
from flask_smorest import Blueprint, abort
from typing import Dict, List

from .schemas.email_schemas import EmailRequestSchema

from dotenv import find_dotenv, dotenv_values

config = dotenv_values(dotenv_path=find_dotenv())

email_blueprint = Blueprint("email", __name__, url_prefix="/email", description="Email API")


@email_blueprint.route("/")
class Email(MethodView):
    url = "https://api.courier.com/send"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['COURIER_API_KEY']}"
    }

    @email_blueprint.arguments(schema=EmailRequestSchema, location="json")
    @email_blueprint.response(status_code=200, description="Email sent successfully")
    def post(self, payload: Dict):
        """
        Send email via courier api
        :return:
        """
        data = payload
        body = f"{data['name']} ({data['email']}) sent you a message: {data['message']}"

        courier_payload = {
            "message": {
                "content": {
                    "title": "Personal Inquiry",
                    "body": body
                },
                "to": {
                    "email": config['PERSONAL_EMAIL']
                }
            }
        }

        confirm_payload = {
            "message": {
                "template": "EHHFDW4D9XMFD6JN0DMWTPREQSXW",
                "to": {
                    "email": data['email']
                }
            }
        }

        try:
            response = requests.post(self.url, headers=self.headers, json=courier_payload)
            if response.status_code == 202:
                confirm_response = requests.post(self.url, headers=self.headers, json=confirm_payload)
                print(confirm_response.json())
                if confirm_response.status_code == 202:
                    return {"message": "Email sent successfully"}

        except (ConnectionError, requests.Timeout, requests.TooManyRedirects) as e:
            print(e)
            abort(500, message="Failed to send email")
