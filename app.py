from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
from lxml import etree
from sqlalchemy import create_engine
from common import CustomLogger, CustomSoap
from prettytable import PrettyTable

from resources.CiscoAXL import *
from resources.CiscoCMS import *

import os
import sys
import json
import zeep

db_connect = create_engine('sqlite:///' + os.path.abspath(os.getcwd()) + '/database.db')

app = Flask(__name__) # pylint: disable=invalid-name
api = Api (app)

#infoLogger = CustomLogger.getCustomLogger('FlaskCiscoCollab', 'FlaskCiscoCollab','DEBUG')
infoLogger = CustomLogger.getCustomLogger('FlaskCiscoCollab', 'FlaskCiscoCollab')

# Rest API para Cisco Unified Communications Manager
api.add_resource(CiscoAXL_Change.CiscoAXL_Change, '/api/v1/CUCM/Change')
api.add_resource(CiscoAXL_CallPickupGroup.CiscoAXL_CallPickupGroup, '/api/v1/CUCM/CallPickupGroup')
api.add_resource(CiscoAXL_Line.CiscoAXL_Line, '/api/v1/CUCM/Line')
api.add_resource(CiscoAXL_Phone.CiscoAXL_Phone, '/api/v1/CUCM/Phone')
api.add_resource(CiscoAXL_ProcessNode.CiscoAXL_ProcessNode, '/api/v1/CUCM/ProcessNode')
api.add_resource(CiscoAXL_RoutePartition.CiscoAXL_RoutePartition, '/api/v1/CUCM/RoutePartition')
api.add_resource(CiscoAXL_ServiceParameter.CiscoAXL_ServiceParameter, '/api/v1/CUCM/ServiceParameter')
api.add_resource(CiscoAXL_Template.CiscoAXL_Template, '/api/v1/CUCM/Template')
api.add_resource(CiscoAXL_TransPattern.CiscoAXL_TransPattern, '/api/v1/CUCM/TransPattern')
api.add_resource(CiscoAXL_User.CiscoAXL_User, '/api/v1/CUCM/User')

api.add_resource(CiscoAXL_File.CiscoAXL_File, '/api/v1/CUCM/File')

# Rest API para Cisco Meeting Server
api.add_resource(CiscoCMS_File.CiscoCMS_File, '/api/v1/CMS/File')

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# *------------------------------------------------------------------
# * Rest API - Cisco AXL - Description
# *
# *  GET    - get    - to retrieve resource representation/information only
# *  POST   - add    - to create new subordinate resources
# *  PUT    - update - to update existing resource
# *  DELETE - remove - to delete resources 
# *  PATCH  - list   - to search resource
# *
# *------------------------------------------------------------------

# *------------------------------------------------------------------
# * Rest API - Cisco AXL - Status Codes
# *
# * - https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
# *------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443, debug=True, ssl_context=context)