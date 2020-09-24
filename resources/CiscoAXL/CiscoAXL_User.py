# -*- coding: utf-8 -*-

# *------------------------------------------------------------------
# * cspaxl_User.py
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

class CiscoAXL_User(Resource):
    def get(self):
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion get de la clase CiscoAXL_User' )
        varFORM = request.form
        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))
        infoLogger.debug('Esta buscando el Userid: %s' % (varFORM['userid']))
        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        CustomSoap_Data = {}

        # Comprobamos si existe la Key userid
        if 'userid' in varFORM:
            CustomSoap_Data['userid'] = varFORM['userid']
        else:
            return {'Class': 'userid','AXL': 'get','Method': 'GET', 'Status': 'ERROR', 'Detail': 'No tenemos el campo userid'},400

        CustomSoap_Data = {
            'userid': varFORM['userid']
        }

        try:
            CustomUser_Resp = CustomService.getUser(**CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            return {'Class': 'userid','AXL': 'get','Method': 'GET', 'Status': 'ERROR', 'Detail': str(sys.exc_info()[1]),'userid':varFORM['userid']},400
        else:
            return json.loads(json.dumps(zeep.helpers.serialize_object(CustomUser_Resp['return'])))

    def post(self):
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoAXL_User' )
        varFORM = request.form
        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))
        infoLogger.debug('Vamos a dar de alta el Userid: %s' % (varFORM['userid']))

        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        CustomSoap_Data = {}

        # Comprobamos si existe la Key lastName
        if 'lastName' in varFORM:
            CustomSoap_Data['lastName'] = varFORM['lastName']
        else:
            return {'Class': 'userid','AXL': 'add','Method': 'POST', 'Status': 'ERROR', 'Detail': 'No tenemos el campo lastName'},400

        # Comprobamos si existe la Key userid
        if 'userid' in varFORM:
            CustomSoap_Data['userid'] = varFORM['userid']
        else:
            return {'Class': 'userid','AXL': 'add','Method': 'POST', 'Status': 'ERROR', 'Detail': 'No tenemos el campo userid'},400

        # Comprobamos si existe la Key presenceGroupName
        if 'presenceGroupName' in varFORM:
            CustomSoap_Data['presenceGroupName'] = varFORM['presenceGroupName']
        else:
            CustomSoap_Data['presenceGroupName'] = 'Standard Presence group'
        if 'pin' in varFORM:
            CustomSoap_Data['pin'] = varFORM['pin']
        else:
            CustomSoap_Data['pin'] = '123456'
        if 'password' in varFORM:
            CustomSoap_Data['password'] = varFORM['password']
        if 'digestCredentials' in varFORM:
            CustomSoap_Data['digestCredentials'] = varFORM['digestCredentials']
        if 'telephoneNumber' in varFORM:
            CustomSoap_Data['telephoneNumber'] = varFORM['telephoneNumber']
            CustomSoap_Data['selfService'] = varFORM['telephoneNumber']
            CustomSoap_Data['enableUserToHostConferenceNow'] = 'true'
            CustomSoap_Data['attendeesAccessCode'] = varFORM['telephoneNumber']

        try:
            # Damos de alta el User ID y no verificamos si existe el mismo User ID
            CustomUser_Resp = CustomService.addUser(CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            return {'Class': 'userid','AXL': 'add','Method': 'POST', 'Status': 'ERROR', 'Detail': str(sys.exc_info()[1]),'userid':varFORM['userid']},400
        else:
            infoLogger.info('Se ha configurado el User ID %s' % (varFORM['userid']))
            return {'Class': 'userid','AXL': 'add','Method': 'POST', 'Status': 'OK', 'Detail': CustomUser_Resp['return'],'userid':varFORM['userid']},201

    def delete(self):
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion delete de la clase CiscoAXL_User' )
        varFORM = request.form
        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))

        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        CustomSoap_Data = {}

        # Comprobamos si existe la Key userid
        if 'userid' in varFORM:
            infoLogger.debug('Vamos a eliminar el Userid: %s' % (varFORM['userid']))
            CustomSoap_Data = {
                'userid': varFORM['userid']
            }
        else:
            return {'Class': 'userid','AXL': 'remove','Method': 'DELETE', 'Status': 'ERROR', 'Detail': 'No tenemos el campo userid'},400

        try:
            CustomUser_Resp = CustomService.removeUser(**CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            return jsonify({'Class': 'userid','AXL': 'remove','Method': 'DELETE', 'Status': 'ERROR', 'Detail': str(sys.exc_info()[1]),'userid':varFORM['userid']})
        else:
            infoLogger.info('Se ha configurado el User ID %s' % (varFORM['userid']))
            return {'Class': 'userid','AXL': 'remove','Method': 'DELETE', 'Status': 'OK', 'Detail': str(CustomUser_Resp['return']),'userid':varFORM['userid']}

    def put(self):
        # * Funcion para actualizar un User
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion put de la clase CiscoAXL_userid' )
        varFORM = request.form
        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))

        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        CustomSoap_Data = {}

        # Comprobamos si existe la Key associatedDevices
        if 'userid' in varFORM:
            CustomSoap_Data = {
                'userid': varFORM['userid'],
              }
        else:
            return {'Class': 'userid','AXL': 'update','Method': 'PUT', 'Status': 'ERROR', 'Detail': 'No esta el campo userid'},400

        try:
            CustomUser_Resp = CustomService.getUser(**CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            return {'Class': 'userid','AXL': 'get','Method': 'GET', 'Status': 'ERROR', 'Detail': str(sys.exc_info()[1]),'userid':varFORM['userid']},400
        else:
            # Comprobamos si existe la Key associatedDevices
            if 'associatedDevices' in varFORM:
                if CustomUser_Resp['return']['user']['associatedDevices'] == None:
                    CustomSoap_Data['associatedDevices'] = {'device': varFORM['associatedDevices']}
                    infoLogger.debug('CustomSoap_Data: %s' % (CustomSoap_Data))
                else:
                    CustomSoap_Data['associatedDevices'] = CustomUser_Resp['return']['user']['associatedDevices']
                    CustomSoap_Data['associatedDevices']['device'].append(varFORM['associatedDevices'][0:15])
                    infoLogger.debug('CustomSoap_Data: %s' % (CustomSoap_Data))
            else:
                return {'Class': 'userid','AXL': 'update','Method': 'PUT', 'Status': 'ERROR', 'Detail': 'No esta definida la funcion'},400

            # Comprobamos si existe la Key pattern y routePartitionName
            if all (k in varFORM for k in ('pattern', 'routePartitionName')):
                    CustomSoap_Data['primaryExtension'] = {
                        'pattern': varFORM['pattern'],
                        'routePartitionName': varFORM['routePartitionName'],
                    }
            try:
                CustomUser_Resp = CustomService.updateUser(**CustomSoap_Data)
            except:
                infoLogger.error('Se ha producido un error en la consulta SOAP')
                infoLogger.debug(sys.exc_info())
                infoLogger.error(sys.exc_info()[1])
                return {'Class': 'User','AXL': 'update','Method': 'POST', 'Status': 'ERROR', 'Detail': str(sys.exc_info()[1]),'userid':varFORM['userid']}
            else:
                infoLogger.info('Se ha actualizado el usuario %s' % (varFORM['userid']))
                return {'Class': 'User','AXL': 'update','Method': 'POST', 'Status': 'OK', 'Detail': str(CustomUser_Resp['return']),'userid':varFORM['userid']},201

    def patch(self):
        # * Funcion para actualizar un User
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion PATCH de la clase CiscoAXL_userid' )
        return {'Class': 'userid','AXL': 'list','Method': 'PATCH', 'Status': 'ERROR', 'Detail': 'No esta definida la funcion'},400
