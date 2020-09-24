# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * cspaxl_File.py
# *
# * Cisco AXL Python
# *
# * Copyright (C) 2015 Carlos Sanz <carlos.sanzpenas@gmail.com>
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
import csv
import sys
import json
import requests
import zeep
import logging

# *------------------------------------------------------------------
# * Rest API - Cisco AXL - Description
# *
# *  GET    - get    - to retrieve resource representation/information only
# *  POST   - add    - to create new subordinate resources
# *  PUT    - update - to update existing resource
# *  DELETE - remove - to delete resources 
# *  PATCH  - list   - to search resource
# *------------------------------------------------------------------

class CiscoUCCX_resourceGroup(Resource):
    def post(self):
        # * Funcion para crear un Resource Group
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoUCCX_resourceGroup' )
        infoLogger.debug('Esta utilizando el metodo POST' )

        varFORM = request.form
        infoLogger.debug('La direccion IP es: %s' % (varFORM))
        #varFORM['mmpHost'] = '10.90.86.7'

        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))
        #if all (k in varFORM for k in ('name')):
        #    infoLogger.info('Se quiere dar de alta el Resource Group %s' % (varFORM['name']))
        #else:
        #    infoLogger.error('No estan todas los parametros requeridos: %s' % (varFORM))
        #    return {'Class': 'CiscoUCCX','UCCX': 'add','Method': 'POST', 'Status': 'ERROR', 'Detail': 'Faltan parametros'},400

        # Variables comunes a todas las peticiones:
        #url = 'https://' + varFORM['mmpHost'] + ':' + varFORM['mmpPort'] + '/api/v1/UCCX/resourceGroup'
        url = 'https://10.90.86.7:' + varFORM['mmpPort'] + '/api/v1/UCCX/resourceGroup'
        headers = {'Content-Type': 'text/xml'}

        # Fichero XML
        xml = """<?xml version="1.0" encoding="UTF-8"?><ResourceGroup><self/><name>' + varFORM['name'] + '</name></ResourceGroup>"""
        infoLogger.debug('XML es %s' % (xml))

        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
        response = requests.post(url, verify=False, headers=headers,data=xml)
        infoLogger.debug('El Response Code es %s' % (response.status_code))
        if response.status_code == 201:
            return {'Class': 'CiscoUCCX','UCCX': 'Add','Method': 'POST', 'Status': 'OK'},response.status_code
        else:
            return {'Class': 'CiscoUCCX','UCCX': 'Add','Method': 'POST', 'Status': 'ERROR'},response.status_code
