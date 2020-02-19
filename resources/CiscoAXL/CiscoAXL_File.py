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
# *
# *------------------------------------------------------------------

class CiscoAXL_File(Resource):
    def post(self):
        # * Funcion para crear un elemento
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoAXL_File' )
        infoLogger.debug('Esta utilizando el metodo POST' )

        if 'File' not in request.files:
            # * La peticion de REST API no tiene un elemento File
            return jsonify({'Class': 'CiscoAXL_File','AXL': 'Add','Method': 'POST', 'Status': 'ERROR: No file attribute'})
        elif request.files['File'].filename == '':
            # * La peticion de REST API no tiene adjunto un fichero.
            return jsonify({'Class': 'CiscoAXL_File','AXL': 'Add','Method': 'POST', 'Status': 'ERROR: No selected file'})

        varFORM = request.form
        varFORMFile = request.files['File']

        # * Subimos el fichero a nuestro Servidor REST API
        varDIR = 'uploads'
        varFORMFile.save(os.path.join(varDIR,varFORMFile.filename))
        varFilename = varDIR + '/' + varFORMFile.filename
        infoLogger.debug('El fichero que vamos a cargar es: %s' % (varFilename))

        try:
            varCSVFile = open(varFilename, 'r', encoding='utf-8')
        except:
            infoLogger.error('Se ha producido un error al abrir el archivo %s' % (varFilename))
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            return jsonify({'Class': 'CiscoAXL_File','AXL': 'Add','Method': 'POST', 'Status': 'ERROR: Can not open the file'})
            sys.exit()
        else:
            infoLogger.info('Se ha abierto el archivo %s' % (varFilename))
            if varFORM['action']  == 'phone':
                # * Damos de alta los telefonos
                varFieldNames = (
                    "FirstName", "Surname", "userPrincipalName", "DirectoryNumber", "Type", "IPPhone", "MACAddress",
                    "IncomingDID", "OutgoingDID", "CSS", "VoiceMail", "CallPickupGroup", "WebUser", "Locale", "ForwardCSS",
                    "CallWaiting", "SRST")
                varFileReader = csv.DictReader(varCSVFile, varFieldNames)
            if varFORM['action']  == 'TransPattern':
                # * Damos de alta los Translation Pattern
                varFileReader = csv.DictReader(varCSVFile)
                # Variables comunes a todas las peticiones:
                url = 'https://127.0.0.1:8443/api/v1/CUCM/TransPattern'
                payloadHeader = 'mmpHost=' + varFORM['mmpHost'] + '&mmpPort=' + varFORM['mmpPort'] + '&mmpUser=' + varFORM['mmpUser'] + '&mmpPass=' + varFORM['mmpPass'].replace('%','%25') + '&mmpVersion=' + varFORM['mmpVersion']
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}

                # Comenzamos el Bucle para dar de alta los Translation Pattern
                for row in varFileReader:
                    infoLogger.debug('Row: %s' % (row))
                    payload = payloadHeader + '&pattern=' + row['pattern'] + '&routePartitionName=' + row['routePartitionName'] + '&callingSearchSpaceName=' + row['callingSearchSpaceName'] + '&calledPartyTransformationMask=' + row['calledPartyTransformationMask']
                    infoLogger.debug('payload: %s' % (payload))
                    response = requests.request('POST', url, verify=False, headers=headers, data = payload)
                    infoLogger.debug('Response: %s' % (json.loads(response.text.encode('utf8'))))
                    #return (json.loads(response.text.encode('utf8')))
            else:
                # * Valor no correcto 
                return jsonify({'Class': 'CiscoAXL_File','AXL': 'Add','Method': 'POST', 'Status': 'ERROR: First row is not valid'})

        finally:
            # * Cerramos el fichero
            varCSVFile.close()
            infoLogger.info('Se ha cerrado el archivo %s' % (varFilename))

        return jsonify({'Class': 'CiscoAXL_File','AXL': 'Add','Method': 'POST', 'Status': 'Ok'})
