from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
from lxml import etree
from sqlalchemy import create_engine
from common import CustomLogger, CustomSoap
from prettytable import PrettyTable

from resources.CiscoAXL import *

import os
import sys
import json
import zeep

db_connect = create_engine('sqlite:///' + os.path.abspath(os.getcwd()) + '/database.db')

app = Flask(__name__) # pylint: disable=invalid-name
api = Api (app)

infoLogger = CustomLogger.getCustomLogger('FlaskCiscoCollab', 'FlaskCiscoCollab','DEBUG')
#infoLogger = CustomLogger.getCustomLogger('FlaskCiscoCollab', 'FlaskCiscoCollab')

api.add_resource(CiscoAXL_Change.CiscoAXL_Change, '/api/v1/CUCM/Change')
api.add_resource(CiscoAXL_Phone.CiscoAXL_Phone, '/api/v1/CUCM/Phone')
api.add_resource(CiscoAXL_ProcessNode.CiscoAXL_ProcessNode, '/api/v1/CUCM/ProcessNode')
api.add_resource(CiscoAXL_ServiceParameter.CiscoAXL_ServiceParameter, '/api/v1/CUCM/ServiceParameter')
api.add_resource(CiscoAXL_Template.CiscoAXL_Template, '/api/v1/CUCM/Template')
api.add_resource(CiscoAXL_TransPattern.CiscoAXL_TransPattern, '/api/v1/CUCM/TransPattern')
api.add_resource(CiscoAXL_User.CiscoAXL_User, '/api/v1/CUCM/User')

@app.route("/", methods=['GET', 'POST', 'PUT'])
def index():
    infoLogger.info('Estoy en la pagina por defecto')
    return render_template("form.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443, debug=True, ssl_context=context)