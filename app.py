from flask import Flask, request, jsonify, redirect, session
from flask_cors import CORS
import requests
import json
# from flask_session import Session
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
import urllib

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mmidwnlqujhcix:37b2d32fb40920701a079e38905616a48223f3896e54aaacee5b2908da205a9f@ec2-44-206-204-65.compute-1.amazonaws.com:5432/dfu2atrj5ad4ef'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = "gtp app"
app.config['DEBUG'] = True
# db = SQLAlchemy(app)
# migrate = Migrate(app,db)
# SESSION_TYPE = 'filesystem'
# app.config.from_object(__name__)
# app.config['SECRET_KEY'] = 'gtpapp'
# Session(app)
CORS(app, origins=['https://gtp-poc.vercel.app','https://fortress-backend-315ca6662153.herokuapp.com'], supports_credentials=True)
ALLOWED_ORIGINS = ["http://localhost:3000","https://gtp-poc.vercel.app","https://fortress-backend-315ca6662153.herokuapp.com", "https://fortress-backend-315ca6662153.herokuapp.com/"]
DOMAIN = "dev-zcni1ru6zcluw75q.jp.auth0.com"
CLIENT_ID = "kU5EZGLslUM30C8MgKqCU37b0sV0JRSL"
CLIENT_SECRET = "inCEaQiCxPyTsY2zFVdSe3dRPhFRBEjn5w6L5IgQc-GDkwICUT785-IhdpEU72CW"
MANAGEMENT_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Il81eko3N2QzYWIxcEh0QUMwMFhoZyJ9.eyJpc3MiOiJodHRwczovL2Rldi16Y25pMXJ1NnpjbHV3NzVxLmpwLmF1dGgwLmNvbS8iLCJzdWIiOiJqWWEyMTU5QmpVTUlqQjV5aTZtZFhrSnNIWEx4UHRhS0BjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9kZXYtemNuaTFydTZ6Y2x1dzc1cS5qcC5hdXRoMC5jb20vYXBpL3YyLyIsImlhdCI6MTcwMTg2NDkwOCwiZXhwIjoxNzA0NDU2OTA4LCJhenAiOiJqWWEyMTU5QmpVTUlqQjV5aTZtZFhrSnNIWEx4UHRhSyIsInNjb3BlIjoicmVhZDpjbGllbnRfZ3JhbnRzIGNyZWF0ZTpjbGllbnRfZ3JhbnRzIGRlbGV0ZTpjbGllbnRfZ3JhbnRzIHVwZGF0ZTpjbGllbnRfZ3JhbnRzIHJlYWQ6dXNlcnMgdXBkYXRlOnVzZXJzIGRlbGV0ZTp1c2VycyBjcmVhdGU6dXNlcnMgcmVhZDp1c2Vyc19hcHBfbWV0YWRhdGEgdXBkYXRlOnVzZXJzX2FwcF9tZXRhZGF0YSBkZWxldGU6dXNlcnNfYXBwX21ldGFkYXRhIGNyZWF0ZTp1c2Vyc19hcHBfbWV0YWRhdGEgcmVhZDp1c2VyX2N1c3RvbV9ibG9ja3MgY3JlYXRlOnVzZXJfY3VzdG9tX2Jsb2NrcyBkZWxldGU6dXNlcl9jdXN0b21fYmxvY2tzIGNyZWF0ZTp1c2VyX3RpY2tldHMgcmVhZDpjbGllbnRzIHVwZGF0ZTpjbGllbnRzIGRlbGV0ZTpjbGllbnRzIGNyZWF0ZTpjbGllbnRzIHJlYWQ6Y2xpZW50X2tleXMgdXBkYXRlOmNsaWVudF9rZXlzIGRlbGV0ZTpjbGllbnRfa2V5cyBjcmVhdGU6Y2xpZW50X2tleXMgcmVhZDpjb25uZWN0aW9ucyB1cGRhdGU6Y29ubmVjdGlvbnMgZGVsZXRlOmNvbm5lY3Rpb25zIGNyZWF0ZTpjb25uZWN0aW9ucyByZWFkOnJlc291cmNlX3NlcnZlcnMgdXBkYXRlOnJlc291cmNlX3NlcnZlcnMgZGVsZXRlOnJlc291cmNlX3NlcnZlcnMgY3JlYXRlOnJlc291cmNlX3NlcnZlcnMgcmVhZDpkZXZpY2VfY3JlZGVudGlhbHMgdXBkYXRlOmRldmljZV9jcmVkZW50aWFscyBkZWxldGU6ZGV2aWNlX2NyZWRlbnRpYWxzIGNyZWF0ZTpkZXZpY2VfY3JlZGVudGlhbHMgcmVhZDpydWxlcyB1cGRhdGU6cnVsZXMgZGVsZXRlOnJ1bGVzIGNyZWF0ZTpydWxlcyByZWFkOnJ1bGVzX2NvbmZpZ3MgdXBkYXRlOnJ1bGVzX2NvbmZpZ3MgZGVsZXRlOnJ1bGVzX2NvbmZpZ3MgcmVhZDpob29rcyB1cGRhdGU6aG9va3MgZGVsZXRlOmhvb2tzIGNyZWF0ZTpob29rcyByZWFkOmFjdGlvbnMgdXBkYXRlOmFjdGlvbnMgZGVsZXRlOmFjdGlvbnMgY3JlYXRlOmFjdGlvbnMgcmVhZDplbWFpbF9wcm92aWRlciB1cGRhdGU6ZW1haWxfcHJvdmlkZXIgZGVsZXRlOmVtYWlsX3Byb3ZpZGVyIGNyZWF0ZTplbWFpbF9wcm92aWRlciBibGFja2xpc3Q6dG9rZW5zIHJlYWQ6c3RhdHMgcmVhZDppbnNpZ2h0cyByZWFkOnRlbmFudF9zZXR0aW5ncyB1cGRhdGU6dGVuYW50X3NldHRpbmdzIHJlYWQ6bG9ncyByZWFkOmxvZ3NfdXNlcnMgcmVhZDpzaGllbGRzIGNyZWF0ZTpzaGllbGRzIHVwZGF0ZTpzaGllbGRzIGRlbGV0ZTpzaGllbGRzIHJlYWQ6YW5vbWFseV9ibG9ja3MgZGVsZXRlOmFub21hbHlfYmxvY2tzIHVwZGF0ZTp0cmlnZ2VycyByZWFkOnRyaWdnZXJzIHJlYWQ6Z3JhbnRzIGRlbGV0ZTpncmFudHMgcmVhZDpndWFyZGlhbl9mYWN0b3JzIHVwZGF0ZTpndWFyZGlhbl9mYWN0b3JzIHJlYWQ6Z3VhcmRpYW5fZW5yb2xsbWVudHMgZGVsZXRlOmd1YXJkaWFuX2Vucm9sbG1lbnRzIGNyZWF0ZTpndWFyZGlhbl9lbnJvbGxtZW50X3RpY2tldHMgcmVhZDp1c2VyX2lkcF90b2tlbnMgY3JlYXRlOnBhc3N3b3Jkc19jaGVja2luZ19qb2IgZGVsZXRlOnBhc3N3b3Jkc19jaGVja2luZ19qb2IgcmVhZDpjdXN0b21fZG9tYWlucyBkZWxldGU6Y3VzdG9tX2RvbWFpbnMgY3JlYXRlOmN1c3RvbV9kb21haW5zIHVwZGF0ZTpjdXN0b21fZG9tYWlucyByZWFkOmVtYWlsX3RlbXBsYXRlcyBjcmVhdGU6ZW1haWxfdGVtcGxhdGVzIHVwZGF0ZTplbWFpbF90ZW1wbGF0ZXMgcmVhZDptZmFfcG9saWNpZXMgdXBkYXRlOm1mYV9wb2xpY2llcyByZWFkOnJvbGVzIGNyZWF0ZTpyb2xlcyBkZWxldGU6cm9sZXMgdXBkYXRlOnJvbGVzIHJlYWQ6cHJvbXB0cyB1cGRhdGU6cHJvbXB0cyByZWFkOmJyYW5kaW5nIHVwZGF0ZTpicmFuZGluZyBkZWxldGU6YnJhbmRpbmcgcmVhZDpsb2dfc3RyZWFtcyBjcmVhdGU6bG9nX3N0cmVhbXMgZGVsZXRlOmxvZ19zdHJlYW1zIHVwZGF0ZTpsb2dfc3RyZWFtcyBjcmVhdGU6c2lnbmluZ19rZXlzIHJlYWQ6c2lnbmluZ19rZXlzIHVwZGF0ZTpzaWduaW5nX2tleXMgcmVhZDpsaW1pdHMgdXBkYXRlOmxpbWl0cyBjcmVhdGU6cm9sZV9tZW1iZXJzIHJlYWQ6cm9sZV9tZW1iZXJzIGRlbGV0ZTpyb2xlX21lbWJlcnMgcmVhZDplbnRpdGxlbWVudHMgcmVhZDphdHRhY2tfcHJvdGVjdGlvbiB1cGRhdGU6YXR0YWNrX3Byb3RlY3Rpb24gcmVhZDpvcmdhbml6YXRpb25zX3N1bW1hcnkgY3JlYXRlOmF1dGhlbnRpY2F0aW9uX21ldGhvZHMgcmVhZDphdXRoZW50aWNhdGlvbl9tZXRob2RzIHVwZGF0ZTphdXRoZW50aWNhdGlvbl9tZXRob2RzIGRlbGV0ZTphdXRoZW50aWNhdGlvbl9tZXRob2RzIHJlYWQ6b3JnYW5pemF0aW9ucyB1cGRhdGU6b3JnYW5pemF0aW9ucyBjcmVhdGU6b3JnYW5pemF0aW9ucyBkZWxldGU6b3JnYW5pemF0aW9ucyBjcmVhdGU6b3JnYW5pemF0aW9uX21lbWJlcnMgcmVhZDpvcmdhbml6YXRpb25fbWVtYmVycyBkZWxldGU6b3JnYW5pemF0aW9uX21lbWJlcnMgY3JlYXRlOm9yZ2FuaXphdGlvbl9jb25uZWN0aW9ucyByZWFkOm9yZ2FuaXphdGlvbl9jb25uZWN0aW9ucyB1cGRhdGU6b3JnYW5pemF0aW9uX2Nvbm5lY3Rpb25zIGRlbGV0ZTpvcmdhbml6YXRpb25fY29ubmVjdGlvbnMgY3JlYXRlOm9yZ2FuaXphdGlvbl9tZW1iZXJfcm9sZXMgcmVhZDpvcmdhbml6YXRpb25fbWVtYmVyX3JvbGVzIGRlbGV0ZTpvcmdhbml6YXRpb25fbWVtYmVyX3JvbGVzIGNyZWF0ZTpvcmdhbml6YXRpb25faW52aXRhdGlvbnMgcmVhZDpvcmdhbml6YXRpb25faW52aXRhdGlvbnMgZGVsZXRlOm9yZ2FuaXphdGlvbl9pbnZpdGF0aW9ucyBkZWxldGU6cGhvbmVfcHJvdmlkZXJzIGNyZWF0ZTpwaG9uZV9wcm92aWRlcnMgcmVhZDpwaG9uZV9wcm92aWRlcnMgdXBkYXRlOnBob25lX3Byb3ZpZGVycyBkZWxldGU6cGhvbmVfdGVtcGxhdGVzIGNyZWF0ZTpwaG9uZV90ZW1wbGF0ZXMgcmVhZDpwaG9uZV90ZW1wbGF0ZXMgdXBkYXRlOnBob25lX3RlbXBsYXRlcyByZWFkOmNsaWVudF9jcmVkZW50aWFscyBjcmVhdGU6Y2xpZW50X2NyZWRlbnRpYWxzIHVwZGF0ZTpjbGllbnRfY3JlZGVudGlhbHMgZGVsZXRlOmNsaWVudF9jcmVkZW50aWFscyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyJ9.Cz2SahVgIjmFyukREowX4_PCVTE1FJbmwh8IppalnLrk8YCGP8ZxTvWMSH5gF-qWNbNXWb4V19U_-ckdjoQIE2Cd7xQCkYYbw2TZYS-If5vz2RnqGYJ2yGmd7OP4QtefzPFEmZa-gXNwmbrkOPPrHQM7i4Q46Pow7xfcb6MJE_Jg38Hh8TYC68vMrKFoQQysVL_5IEccdM7EZU0t7Zrp1-ekdgvg3Jft2etaNCeJJ0CMK0WTla4ykMGqOmJAYgelgx6-ZdaxXRO6s_UmQdCJlLt6_nLqxQ40T6jsyYBbdhXsT1kANiiZKAN0p_jjOCWmxCTIrM8tvOXDix2S9_fgtA"
USER = {
    "access_token": "",
    "id_token": ""
}

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     name = db.Column(db.String(50))
#     email = db.Column(db.String(50), unique=True)
#     user_id = db.Column(db.String(50), unique=True, nullable=False)
#     access_token = db.Column(db.Text())
#     id_token = db.Column(db.Text())
#     is_authenticated = db.Column(db.Boolean, default=False)

# db.create_all()

#                                            Auth0 APIs

#                                            Lookup a user in Auth0 API

def lookupInAuth0(data):
    url = f"https://dev-zcni1ru6zcluw75q.jp.auth0.com/api/v2/users"
    payload = {}
    params = {
        'q': data['email'],
    }
    headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {data["ManagementToken"]}'
    }

    response = requests.get(url = url, headers=headers, json=payload ,params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to call external API. Status: {response}"}

@app.route('/api/lookupUserInAuth0', methods=['OPTIONS', 'POST'])
def lookup_in_auth0():
    try:
        data = request.get_json()

        if 'ManagementToken' in data:
            external_api_response = lookupInAuth0(data)
            return jsonify(external_api_response)
        else:
            return jsonify({"error": "Missing 'ManagementToken' in the request data"})

    except Exception as e:
        return jsonify({"error": str(e)})


#                                            Reset password in Auth0 API

def reset_password_auth0(data):

    url = "https://dev-zcni1ru6zcluw75q.jp.auth0.com/dbconnections/change_password"
    headers = {
        'content-type': 'application/json',
    }

    payload = {
        'client_id': 'kU5EZGLslUM30C8MgKqCU37b0sV0JRSL',
        'email': data["email"],
        'connection': 'Username-Password-Authentication',
    }

    response = requests.post(url=url, headers=headers, json=payload)

    if response.status_code == 200:
        return {"status":response.status_code}
    else:
        return {"error": f"Failed to call external API. Status: {response}"}



@app.route('/api/resetPasswordInAuth0', methods=['OPTIONS', 'POST'])
def reset_password_in_auth0():
    try:
        data = request.get_json()
        if 'email' in data:
            external_api_response = reset_password_auth0(data)
            return jsonify(external_api_response)
        else:
            return jsonify({"error": "Missing 'email' in the request data"})

    except Exception as e:
        return jsonify({"error": str(e)})

#                                            Link user in Auth0 API


def linkUserInAuth0(data):
    url = f"https://dev-zcni1ru6zcluw75q.jp.auth0.com/api/v2/users/auth0%7C655508d3c5d047759db3a83f/identities"

    payload = json.dumps({
    "provider": data["provider"],
    "user_id": data["user_id"]
    })

    headers = {
    'Authorization': f'Bearer {data["ManagementToken"]}',
    'Content-Type': 'application/json',
    'Accept': 'application/json',
   }

    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to call external API. Status: {response}"}

@app.route('/api/linkUser', methods=['OPTIONS', 'POST'])
def link_user_in_auth0():
    try:
        data = request.get_json()

        if 'ManagementToken' in data:
            external_api_response = linkUserInAuth0(data)
            return jsonify(external_api_response)
        else:
            return jsonify({"error": "Missing 'ManagementToken' in the request data"})

    except Exception as e:
        return jsonify({"error": str(e)})



#                                            Capillary APIs

#                                            Capillary Lookup API

def lookupInCapillary(data):
    url = 'https://apac.api.capillarytech.com/v2/customers/lookup/customerDetails'
    headers = {
    'Authorization': 'Basic ZGVtby5mb3J0cmVzcy5zb2x1dGlvbnM6ZjdiMDg4YjYwNjNmN2RjZWIzNjY4YzdkMjk2MzM0Y2I=',
    }

    params = {
        'source': 'INSTORE',
        'identifierName': data['identifierName'],
        'identifierValue': data['identifierValue'],
    }

    response = requests.get(url=url,
        params=params,
        headers=headers,
    )

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to call external API. Status: {response}"}


@app.route('/api/lookupInCapillary', methods=['OPTIONS', 'POST'])
def capillary_lookup():

    try:
        data = request.get_json()
        if 'identifierValue' in data:
            external_api_response = lookupInCapillary(data)
            return jsonify(external_api_response)
        else:
            return jsonify({"error": "Missing 'identifierValue' in the request data"})

    except Exception as e:
        return jsonify({"error": str(e)})


#                                            Get User from Capillary API


def getUserFromCapillary(data):
    api_url = 'https://apac.api.capillarytech.com/mobile/v2/api/customer/getbyemail'
    headers = {
        'CAP_BRAND': 'FORTRESSDEMO',
        'X-CAP-EXTERNAL-OAUTH-ID-TOKEN': data["X-CAP-EXTERNAL-OAUTH-ID-TOKEN"],
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {data["Authorization"]}'
    }

    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to call external API. Status code: {response.status_code}"}


@app.route('/api/getCustomer', methods=['OPTIONS', 'POST'])
def get_customer_from_capillary():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Preflight request successful','status':"success"})
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, X-CAP-EXTERNAL-OAUTH-ID-TOKEN')

        return response

    try:
        data = request.get_json()

        if 'Authorization' in data:
            external_api_response = getUserFromCapillary(data)
            return jsonify(external_api_response)
        else:
            return jsonify({"error": "Missing 'Authorization' in the request data"})

    except Exception as e:
        return jsonify({"error": str(e)})



#                                            Create  User in Capillary API

def createUserInCapillary(data):
    api_url = 'https://apac.api.capillarytech.com/mobile/v2/api/v2/ciamcustomers/add'
    headers = {
        'CAP_BRAND': 'FORTRESSDEMO',
        'X-CAP-EXTERNAL-OAUTH-ID-TOKEN': data["X-CAP-EXTERNAL-OAUTH-ID-TOKEN"],
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {data["Authorization"]}'
    }

    response = requests.post(api_url, headers=headers, json={})

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to call external API. Status code: {response}"}

@app.route('/')
def hello():
    return "Hello Fortress world"

@app.route('/home')
def hello1():
    return "Hello home page"

@app.route('/api/addCustomer', methods=['OPTIONS', 'POST'])
def add_customer_in_capillary():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Preflight request successful','status':"success"})
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, X-CAP-EXTERNAL-OAUTH-ID-TOKEN')
        return response

    try:
        data = request.get_json()

        if 'Authorization' in data:
            external_api_response = createUserInCapillary(data)
            return jsonify(external_api_response)
        else:
            return jsonify({"error": "Missing 'Authorization' in the request data"})

    except Exception as e:
        return jsonify({"error": str(e)})


#                                            Update Customer in Capillary API


def updateUserInCapillary(data,userDetails):
    api_url = 'https://apac.api.capillarytech.com/mobile/v2/api/ciamcustomer/v1update'
    headers = {
        'CAP_BRAND': 'FORTRESSDEMO',
        'X-CAP-EXTERNAL-OAUTH-ID-TOKEN': data["X-CAP-EXTERNAL-OAUTH-ID-TOKEN"],
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {data["Authorization"]}'
    }
    json_data = userDetails
    response = requests.post(api_url, headers=headers,json=json_data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to call external API. Status code: {response.status_code}"}

@app.route('/api/updateCustomer', methods=['OPTIONS', 'POST'])
def update_customer_in_capillary():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Preflight request successful','status':"success"})
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, X-CAP-EXTERNAL-OAUTH-ID-TOKEN')

        return response

    try:
        data = request.get_json()

        if 'Authorization' in data:
            external_api_response = updateUserInCapillary(data,data["user"])
            return jsonify(external_api_response)
        else:
            return jsonify({"error": "Missing 'Authorization' in the request data"})

    except Exception as e:
        return jsonify({"error": str(e)})



#                                            Update Customer with card in Capillary API


def updateUserInCapillaryWithCardnumber(userDetails):
    headers = {
    'Authorization': 'Basic ZGVtby5mb3J0cmVzcy5zb2x1dGlvbnM6ZjdiMDg4YjYwNjNmN2RjZWIzNjY4YzdkMjk2MzM0Y2I=',
    'Content-Type': 'application/json',
    }

    params = {
        'format': 'json',
    }
    json_data = userDetails

    response = requests.post('https://apac.api.capillarytech.com/v1.1/customer/update', params=params, headers=headers, json=json_data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to call external API. Status code: {response.status_code}"}

@app.route('/api/updateCustomerWithCardNumber', methods=['OPTIONS', 'POST'])
def update_customer_in_capillary_with_cardnumber():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Preflight request successful','status':"success"})
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, X-CAP-EXTERNAL-OAUTH-ID-TOKEN')

        return response

    try:
        data = request.get_json()

        if 'user' in data:
            external_api_response = updateUserInCapillaryWithCardnumber(data["user"])
            return jsonify(external_api_response)
        else:
            return jsonify({"error": "Missing 'user' in the request data"})
    except Exception as e:
        return jsonify({"error": str(e)})

#                                       Add Customer in Capillary as non-loyalty API
def addUserInCapillaryWithBasicAuth(userDetails):
    headers = {
    'Authorization': 'Basic ZGVtby5mb3J0cmVzcy5zb2x1dGlvbnM6ZjdiMDg4YjYwNjNmN2RjZWIzNjY4YzdkMjk2MzM0Y2I=',
    'Content-Type': 'application/json',
    }

    params = {
        'format': 'json',
    }
    json_data = userDetails

    response = requests.post('https://apac.api.capillarytech.com/v1.1/customer/add', params=params, headers=headers, json=json_data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to call external API. Status code: {response.status_code}"}

@app.route('/api/addCustomerBasicAuth', methods=['OPTIONS', 'POST'])
def add_customer_in_capillary_basic_auth():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Preflight request successful','status':"success"})
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, X-CAP-EXTERNAL-OAUTH-ID-TOKEN')
        return response

    try:
        data = request.get_json()

        if 'user' in data:
            external_api_response = addUserInCapillaryWithBasicAuth(data["user"])
            return jsonify(external_api_response)
        else:
            return jsonify({"error": "Missing 'user' in the request data"})
    except Exception as e:
        return jsonify({"error": str(e)})

# @app.route('/generic_callback', methods=['POST', 'GET'])
@app.route('/generic_callback')
def get_generic_callback():
    """
    Method to handle generic callbacks from logins.

    Expects
    Method:          POST
    Data:            payload, data
    """

    # if request.method == 'GET':
    #     return "Get method is working fine"
    # else:
    try:
        logger.info("<-- Logger statements start for callback --> ")
        state = request.args.get('state')
        code = request.args.get('code')
        logger.info("state --> ",state)
        logger.info("code --> ",code)
        logger.info("<-- Logger statements end for callback --> ")
        print({
            "state": state,
            "code": code
        })
        return jsonify({
            "state": state,
            "code": code
        })
    except Exception as e:
        return jsonify({"error": str(e)})

#                                  User profile sync between CAP and Auth0

def userProfileUpdateInAuth0(data):
    user_id = data["user_id"]
    user_id = urllib.parse.quote(user_id)
    url = f"https://dev-zcni1ru6zcluw75q.jp.auth0.com/api/v2/users/{user_id}"

    payload = json.dumps({
        "email": data['email']
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {data["ManagementToken"]}'
    }

    response = requests.request("PATCH", url, headers=headers, data=payload)
    return response.json()

@app.route('/customer_update', methods=['OPTIONS', 'POST', 'GET'])
def customer_update_auth0_from_capillary():
    """
    Method to handle events coming from Capillary & update back in Auth0.

    Expects
    Method:          POST
    Data:            payload, data
    """

    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Preflight request successful', 'status': "success"})
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, X-CAP-EXTERNAL-OAUTH-ID-TOKEN')

        return response

    if request.method == "GET":
        return "GET Method is working fine"

    try:
        data = request.get_json()
        # logger.info("<-- Logger statements start for callback --> ")
        #
        # print("external_api_response from print stmt DATA==> ",data )
        # print("external_api_response from print UPDATED FIELDS stmt ==>",data["data"]['updatedFields'])
        # print("external_api_response from print PREVIOUS VALUE stmt ==>",data["data"]['updatedFields'][0]["previousValue"])
        # logger.info("logger output --> ", data["data"]['updatedFields'][0]["previousValue"])
        # logger.info("<-- Logger statements end for callback --> ")
        updated_email = data["data"]['updatedFields'][0]["previousValue"]
        current_email = data["data"]['updatedFields'][0]["currentValue"]

        body = {
            "ManagementToken": MANAGEMENT_TOKEN,
            "email": updated_email
        }

        external_api_response = lookupInAuth0(body)
        body_for_user_update = {
            "ManagementToken" : body["ManagementToken"],
            "email": current_email,
            "user_id": external_api_response[0]["user_id"]
        }
        userUpdateResponse = userProfileUpdateInAuth0(body_for_user_update)
        return jsonify({"eventDetails":userUpdateResponse})
    except Exception as e:
        print("Error --> ", str(e))
        return jsonify({"error": str(e)})


@app.route('/auth0_callback',methods=['OPTIONS', 'POST', 'GET'])
def auth0_callback():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'Preflight request successful', 'status': "success"})
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, X-CAP-EXTERNAL-OAUTH-ID-TOKEN')

        return response
    try:
        if request.method == "GET":
            print("Auth0 Callback Details:")
            print("####################################")
            code = request.args.get('code')
            state = request.args.get('state')
            print("Code:", code)
            print("State:", state)
            authorization_code = request.args.get('code')
            token_url = f'https://{DOMAIN}/oauth/token'
            client_id = CLIENT_ID
            client_secret = CLIENT_SECRET
            redirect_uri = 'https://fortress-backend-315ca6662153.herokuapp.com'

            payload = {
                'grant_type': 'authorization_code',
                'client_id': client_id,
                'client_secret': client_secret,
                'code': authorization_code,
                'redirect_uri': redirect_uri
            }

            response = requests.post(token_url, json=payload)
            if response.status_code == 200:
                access_token = response.json().get('access_token')
                id_token = response.json().get('id_token')

                print("############### ACCESS TOKEN ####################")
                print(access_token)
                # session['token'] = {
                #     'access_token' : access_token,
                #     'id_token': id_token
                # }
                # session['username'] = user['username']
                # USER["access_token"] = access_token
                # USER["id_token"] = id_token
                user_info = getUserInfoFromAuth0()
                management_user_info = getManagementUserInfoFromAuth0(user_info['sub'])
                print(user_info)
                print(management_user_info)
                # session['token']["user_object"] = {
                #   'email': management_user_info['email'],
                #   'name': management_user_info['name'],
                #   'user_id': management_user_info['user_id']
                # }
                # user = User.query.filter_by(email=management_user_info['email']).first()
                # if user:
                #     user.is_authenticated = True
                #     db.session.add(user)
                #     db.session.commit()

                # else:
                #     user = User(
                #         username=management_user_info['user_id'],
                #         name = management_user_info['name'],
                #         user_id = management_user_info['user_id'],
                #         email = management_user_info['email'],
                #         access_token = access_token,
                #         id_token = id_token,
                #         is_authenticated = True
                #         )
                #     db.session.add(user)
                #     db.session.commit()
                #     print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                #     print(User.query.all())
                #     print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

    
                # session['token']["user_object"] = {
                #   'email': 'masdjk',
                #   'name': 'asd',
                #   'user_id': 'asdljasd'
                # }
                # print("************************")
                # print(session)
                # print(session.get('token')['access_token'])
                # print("************************")

                print("############### ACCESS TOKEN ####################")
                return redirect(f"https://gtp-poc.vercel.app/?user={management_user_info['user_id']}", code=302)
            else:
                return 'Token exchange failed'
    
    except Exception as e:
        print("Error --> ", str(e))
        return jsonify({"error": str(e)})

def getUserInfoFromAuth0():
    url = f'https://{DOMAIN}/userinfo'
    headers = {
    'Authorization': f"Bearer {session.get('token')['access_token']}"
    }
    response = requests.get(url = url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to call external API. Status: {response}"}

def getManagementUserInfoFromAuth0(user_id):
    url = f"https://{DOMAIN}/api/v2/users/{user_id}"

    payload = {}
    headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {MANAGEMENT_TOKEN}'
    }

    response = requests.request("GET", url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to call external API. Status: {response}"}




@app.route('/getUserAuthStatus/<user_id>',methods=['OPTIONS','GET'])
def get_user_auth_status(user_id):
    # if request.method == 'OPTIONS':
    #     response = jsonify({'message': 'Preflight request successful','status':"success"})
    #     response.headers.add('Access-Control-Allow-Origin', 'https://gtp-poc.vercel.app/')
    #     return response
    print('^^^^^^^^^^^^^^^^^^^')
    print(user_id)
    if 'token' in session:
        user = session['token']
        return jsonify({'authenticated': True, 'user': user})
    else:
        return jsonify({'authenticated': False})

    # return jsonify(session.get('token'))

@app.route('/check-auth')
def check_auth():
    auth_tokens = request.cookies.get('auth_tokens')

    if auth_tokens:
        print(auth_tokens)
        return jsonify({'authenticated': True, 'user':auth_tokens })

    return jsonify({'authenticated': False})

@app.route('/logout/<email>')
def logout(email):
    # user = User.query.filter_by(email=email).first()
    # if user:
    #     user.is_authenticated = False
    #     db.session.add(user)
    #     db.session.commit()
    # Clear the user's session
    # session.pop('token', None)
    return jsonify({'message': 'Logout successful'})

@app.route('/api/getAuthTokens',methods=['OPTIONS', 'POST'])
def getAuthTokens():
    if request.method == 'OPTIONS':
            response = jsonify({'message': 'Preflight request successful', 'status': "success"})
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type, X-CAP-EXTERNAL-OAUTH-ID-TOKEN')
            return response
    if request.method == 'POST':
        try:
            token_url = f'https://{DOMAIN}/oauth/token'
            client_id = CLIENT_ID
            client_secret = CLIENT_SECRET
            redirect_uri = 'https://gtp-poc.vercel.app/callback'
            data = request.get_json()
            payload = {
                'grant_type': 'authorization_code',
                'client_id': client_id,
                'client_secret': client_secret,
                'code': data['code'],
                'redirect_uri': redirect_uri
            }

            response = requests.post(token_url, json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to call external API. Status: {response}"}
        except Exception as e:
            print("Error --> ", str(e))
            return jsonify({"error": str(e)})
if __name__ == '__main__':
    app.run(debug=False)
