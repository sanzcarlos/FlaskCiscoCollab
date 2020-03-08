# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * cspaxl_ServiceParameter.py
# *
# * Cisco AXL Python
# *
# * Copyright (C) 2020 Carlos Sanz <carlos.sanzpenas@gmail.com>
# *
# *  This program is free software; you can redistribute it and/or
# * modify it under the terms of the GNU General Public License
# * as published by the Free Software Foundation; either version 2
# * of the License, or (at your option) any later version.
# *
# *  This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# * GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# *------------------------------------------------------------------
# *

# Import Modules
from flask import jsonify
from flask_restful import Resource
from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
from lxml import etree
from common import CustomLogger, CustomSoap

import os
import sys
import json
import zeep
import logging

class CiscoAXL_ServiceParameter(Resource):
    def get(self):
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion get de la clase CiscoAXL_ServiceParameter' )
        return jsonify({'Class': 'ServiceParameter','AXL': 'Get','Method': 'GET', 'Status': 'Ok'})

    def post(self):
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoAXL_ServiceParameter' )
        return jsonify({'Class': 'ServiceParameter','AXL': 'Add','Method': 'POST', 'Status': 'Ok'})

    def patch(self):
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoAXL_ServiceParameter' )
        return jsonify({'Class': 'ServiceParameter','AXL': 'List','Method': 'PATCH', 'Status': 'Ok'})

    def put(self):
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion put de la clase CiscoAXL_ServiceParameter' )
        return jsonify({'Class': 'ServiceParameter','AXL': 'Update','Method': 'PUT', 'Status': 'Ok'})

    def delete(self):
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion delete de la clase CiscoAXL_ServiceParameter' )
        return jsonify({'Class': 'ServiceParameter','AXL': 'Remove','Method': 'DELETE', 'Status': 'Ok'})