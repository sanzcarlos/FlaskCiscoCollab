# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * cspaxl_File.py
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
            return jsonify({'Class': 'CiscoAXL_File','AXL': 'Add','Method': 'POST', 'Status': 'ERROR: No file attribute'}),400
        elif request.files['File'].filename == '':
            # * La peticion de REST API no tiene adjunto un fichero.
            return jsonify({'Class': 'CiscoAXL_File','AXL': 'Add','Method': 'POST', 'Status': 'ERROR: No selected file'}),400

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
            return jsonify({'Class': 'CiscoAXL_File','AXL': 'Add','Method': 'POST', 'Status': 'ERROR: Can not open the file'}),406
            sys.exit()
        else:
            infoLogger.info('Se ha abierto el archivo %s' % (varFilename))
            if varFORM['action']  == 'Phone':
                # * Damos de alta los telefonos
                varFileReader = csv.DictReader(varCSVFile)
                # Variables comunes a todas las peticiones:
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                # Comenzamos el Bucle para dar de alta los Directory Number y los Telefono
                result = {}
                i = 1
                for row in varFileReader:
                    payload = 'mmpHost=' + varFORM['mmpHost'] + '&mmpPort=' + varFORM['mmpPort'] + '&mmpUser=' + varFORM['mmpUser'] + '&mmpPass=' + varFORM['mmpPass'].replace('%','%25') + '&mmpVersion=' + varFORM['mmpVersion']
                    # Damos de alta la linea
                    url = 'https://127.0.0.1:8443/api/v1/CUCM/Line'
                    if 'FirstName' in row:
                        if 'Surname' in row:
                            payload = payload + '&description=' + row['FirstName'] + ' ' + row['Surname'] + '&alertingName=' + row['FirstName'] + ' ' + row['Surname']
                    if 'routePartitionName' in row:
                        payload = payload + '&routePartitionName=' + row['routePartitionName']
                    if 'shareLineAppearanceCssName' in row:
                        payload = payload + '&shareLineAppearanceCssName=' + row['shareLineAppearanceCssName']
                    if 'pattern' in row:
                        payload = payload + '&pattern=' + row['pattern']
                    if 'e164Mask' in row:
                        payload = payload + '&e164Mask=' + row['e164Mask']
                    if 'callForwardAll' in row:
                        if 'callingSearchSpaceName' in row:
                            payload = payload + '&callForwardAll=' + row['callForwardAll'] + '&callingSearchSpaceName=' + row['callingSearchSpaceName']
                        else:
                            payload = payload + '&callForwardAll=' + row['callForwardAll']
                    if 'callPickupGroupName' in row:
                        payload = payload + '&callPickupGroupName=' + row['callPickupGroupName']
                    infoLogger.debug('payload: %s' % (payload))
                    response = requests.request('POST', url, verify=False, headers=headers, data = payload)
                    infoLogger.debug('Response: %s' % (json.loads(response.text.encode('utf8'))))
                    result['Line' + str(i)] = json.loads(response.text.encode('utf8'))

                    # Damos de alta el Telefono
                    url = 'https://127.0.0.1:8443/api/v1/CUCM/Phone'
                    if 'IPPhone' in row:
                        if row['IPPhone'][0:2] == '39' or \
                            row['IPPhone'][0:2] == '78' or \
                            row['IPPhone'][0:2] == '88' or \
                            row['IPPhone'][0:2] == '99' or \
                            row['IPPhone'][0:7] == 'ATA 190':
                            payload = payload + '&protocol=SIP&product=Cisco ' + row['IPPhone']
                            infoLogger.debug('payload: %s' % (payload))
                        # Definición Cisco Unified Client Services Framework
                        elif row['IPPhone'][0:3] == 'CSF':
                            payload = payload + '&protocol=SIP&product=Cisco Unified Client Services Framework'                        
                            infoLogger.debug('payload: %s' % (payload))
                        # Definición Third-party SIP Device (Advanced)
                        elif row['IPPhone'][0:3] == 'SIP':
                            payload = payload + '&protocol=SIP&product=Third-party SIP Device (Advanced)'
                            infoLogger.debug('payload: %s' % (payload))
                        # Definición de maxNumCalls y busyTrigger
                        else:
                            payload = payload + '&protocol=SCCP&product=Cisco ' + row['IPPhone']
                            infoLogger.debug('payload: %s' % (payload))
                        # Definición de maxNumCalls y busyTrigger
                        if row['IPPhone'][0:2] == '39' or \
                            row['IPPhone'][0:3] == 'ATA':
                            row['maxNumCalls']='2'
                            row['busyTrigger']='1'
                        else:
                            row['maxNumCalls']='4'
                            row['busyTrigger']='2'
                    else:
                        infoLogger.error('No esta el campo IPPhone: %s' % (row))
                        return {'Class': 'Phone','AXL': 'add','Method': 'POST', 'Status': 'ERROR', 'Detail': 'Faltan el parametro IPPhone'},400

                    # Comprobamos si existe la Key userPrincipalName
                    if 'userPrincipalName' in row:
                        payload = payload + '&ownerUserName=' + row['userPrincipalName']+ '&userid=' + row['userPrincipalName']
                    if 'digestUser' in row:
                        payload = payload + '&digestUser=' + row['digestUser']
                            
                    # Comprobamos si existe la Key name, devicePoolName, commonPhoneConfigName, locationName, phoneTemplateName
                    if all (k in row for k in ('name', 'devicePoolName', 'commonPhoneConfigName','locationName', 'phoneTemplateName', 'routePartitionName')):
                        payload = payload + '&name=' + row['name'] + '&devicePoolName=' + row['devicePoolName'] + '&commonPhoneConfigName=' + row['commonPhoneConfigName'] + '&locationName=' + row['locationName'] + '&phoneTemplateName=' + row['phoneTemplateName'] + '&lines=' + row['pattern'] + '&routePartitionName=' + row['routePartitionName']
                    else:
                        infoLogger.error('No estan todas los parametros requeridos: %s' % (row))
                        return {'Class': 'Phone','AXL': 'add','Method': 'POST', 'Status': 'ERROR', 'Detail': 'Falta alguno de los siguientes parametros parametros: name, devicePoolName, commonPhoneConfigName, locationName, phoneTemplateName'},400
                    infoLogger.debug('payload: %s' % (payload))
                    response = requests.request('POST', url, verify=False, headers=headers, data = payload)
                    infoLogger.debug('Response: %s' % (json.loads(response.text.encode('utf8'))))
                    result['Phone' + str(i)] = json.loads(response.text.encode('utf8'))

                    # Actualizamos el usuario
                    url = 'https://127.0.0.1:8443/api/v1/CUCM/User'

                    if 'userPrincipalName' in row:
                        payload = payload + '&associatedDevices=' + row['name']
                    else:
                        infoLogger.error('No estan todas los parametros requeridos: %s' % (row))
                        return {'Class': 'User','AXL': 'update','Method': 'PUT', 'Status': 'ERROR', 'Detail': 'Falta alguno el parametros: userPrincipalName'},400
                    infoLogger.debug('payload: %s' % (payload))
                    response = requests.request('PUT', url, verify=False, headers=headers, data = payload)
                    infoLogger.debug('Response: %s' % (json.loads(response.text.encode('utf8'))))
                    result['User' + str(i)] = json.loads(response.text.encode('utf8'))

                    i = i + 1
                return (json.loads(json.dumps(result)))

            elif varFORM['action']  == 'TransPattern':
                # * Damos de alta los Translation Pattern
                varFileReader = csv.DictReader(varCSVFile)
                # Variables comunes a todas las peticiones:
                url = 'https://127.0.0.1:8443/api/v1/CUCM/TransPattern'
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}

                # Comenzamos el Bucle para dar de alta los Translation Pattern
                result = {}
                i = 1
                for row in varFileReader:
                    payload = 'mmpHost=' + varFORM['mmpHost'] + '&mmpPort=' + varFORM['mmpPort'] + '&mmpUser=' + varFORM['mmpUser'] + '&mmpPass=' + varFORM['mmpPass'].replace('%','%25') + '&mmpVersion=' + varFORM['mmpVersion']
                    if 'pattern' in row:
                        payload = payload + '&pattern=' + row['pattern']
                    if 'description' in row:
                        payload = payload + '&description=' + row['description']
                    if 'routePartitionName' in row:
                        payload = payload + '&routePartitionName=' + row['routePartitionName']
                    if 'callingSearchSpaceName' in row:
                        payload = payload + '&callingSearchSpaceName=' + row['callingSearchSpaceName']
                    if 'calledPartyTransformationMask' in row:
                        payload = payload + '&calledPartyTransformationMask=' + row['calledPartyTransformationMask']
                    if 'patternUrgency' in row:
                        payload = payload + '&patternUrgency=' + row['patternUrgency']
                    if 'provideOutsideDialtone' in row:
                        payload = payload + '&provideOutsideDialtone=' + row['provideOutsideDialtone']
                    response = requests.request('POST', url, verify=False, headers=headers, data = payload)
                    infoLogger.debug('Response: %s' % (json.loads(response.text.encode('utf8'))))
                    result[i] = json.loads(response.text.encode('utf8'))
                    i = i + 1
                return (json.loads(json.dumps(result)))
            elif varFORM['action']  == 'Users':
                # * Damos de alta los Endusers
                varFileReader = csv.DictReader(varCSVFile)
                # Variables comunes a todas las peticiones:
                url = 'https://127.0.0.1:8443/api/v1/CUCM/User'
                headers = {'Content-Type': 'application/x-www-form-urlencoded'}

                # Comenzamos el Bucle para dar de alta los Users
                result = {}
                i = 1
                for row in varFileReader:
                    payload = 'mmpHost=' + varFORM['mmpHost'] + '&mmpPort=' + varFORM['mmpPort'] + '&mmpUser=' + varFORM['mmpUser'] + '&mmpPass=' + varFORM['mmpPass'].replace('%','%25') + '&mmpVersion=' + varFORM['mmpVersion']
                    if 'userid' in row:
                        payload = payload + '&userid=' + row['userid']
                    if 'lastName' in row:
                        payload = payload + '&lastName=' + row['lastName']
                    if 'password' in row:
                        payload = payload + '&password=' + row['password'] + '&digestCredentials=' + row['password'] + '&pin=123456'
                    if 'telephoneNumber' in row:
                        payload = payload + '&telephoneNumber=' + row['telephoneNumber']
                    response = requests.request('POST', url, verify=False, headers=headers, data = payload)
                    print (response)
                    infoLogger.debug('Response: %s' % (json.loads(response.text.encode('utf8'))))
                    result[i] = json.loads(response.text.encode('utf8'))
                    i = i + 1
                return (json.loads(json.dumps(result)))
            else:
                # * Valor no correcto 
                return jsonify({'Class': 'CiscoAXL_File','AXL': 'Add','Method': 'POST', 'Status': 'ERROR: First row is not valid'}),400

        finally:
            # * Cerramos el fichero
            varCSVFile.close()
            infoLogger.info('Se ha cerrado el archivo %s' % (varFilename))

        return jsonify({'Class': 'CiscoAXL_File','AXL': 'Add','Method': 'POST', 'Status': 'Ok'})
