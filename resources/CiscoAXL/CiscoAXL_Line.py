# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * cspaxl_Line.py
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

class CiscoAXL_Line(Resource):
    def get(self):
        # * Funcion para obtener todos los datos de un Directory Number
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion get de la clase CiscoAXL_Line' )
        varFORM = request.form
        if all (k in varFORM for k in ('pattern', 'routePartitionName')):
            infoLogger.debug('Esta buscando el Directory Number %s en la Particion %s' % (varFORM['pattern'],varFORM['routePartitionName']))
            CustomSoap_Data = {
                    'pattern': varFORM['pattern'],
                    'routePartitionName': varFORM['routePartitionName']
            }
        else:
            infoLogger.error('No estan todas los parametros requeridos: %s' % (varFORM))
            return {'Class': 'line','AXL': 'get','Method': 'GET', 'Status': 'ERROR', 'Detail': 'Faltan parametros'},400

        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))
        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        try:
            CustomUser_Resp = CustomService.getLine(**CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            infoLogger.error(type(zeep.helpers.serialize_object(sys.exc_info()[1])))
            return {'Class': 'line','AXL': 'get','Method': 'GET', 'Status': 'ERROR', 'Detail': str(sys.exc_info()[1]),'pattern':varFORM['pattern'],'routePartitionName':varFORM['routePartitionName']},400
        else:
            infoLogger.info('Se ha encontrado el Translation Pattern %s en la Particion %s' % (varFORM['pattern'],varFORM['routePartitionName']))
            return json.loads(json.dumps(zeep.helpers.serialize_object(CustomUser_Resp['return'])))

    def post(self):
        # * Funcion para crear un Directory Number
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoAXL_Line' )
        varFORM = request.form
        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))
        if all (k in varFORM for k in ('pattern', 'routePartitionName')):
            infoLogger.debug('Se quiere dar de alta el Directory Number %s en la Particion %s' % (varFORM['pattern'],varFORM['routePartitionName']))
            CustomSoap_Data = {
                    'pattern': varFORM['pattern'],
                    'routePartitionName': varFORM['routePartitionName']
            }
        else:
            infoLogger.error('No estan todas los parametros requeridos: %s' % (varFORM))
            return {'Class': 'line','AXL': 'add','Method': 'POST', 'Status': 'ERROR', 'Detail': 'Faltan parametros'},400

        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        # Comprobamos si existe la Key usage
        if 'usage' in varFORM:
            CustomSoap_Data['usage'] = varFORM['usage']
        else:
            CustomSoap_Data['usage'] = 'Device'

        # Comprobamos si existe la Key description
        if 'description' in varFORM:
            CustomSoap_Data['description'] = varFORM['description']

        # Comprobamos si existe la Key alertingName
        if 'alertingName' in varFORM:
            CustomSoap_Data['alertingName'] = varFORM['alertingName']

        # Comprobamos si existe la Key voiceMailProfileName
        if 'voiceMailProfileName' in varFORM:
            CustomSoap_Data['voiceMailProfileName'] = varFORM['voiceMailProfileName']

        # Comprobamos si existe la Key allowCtiControlFlag
        if 'allowCtiControlFlag' in varFORM:
            CustomSoap_Data['allowCtiControlFlag'] = varFORM['allowCtiControlFlag']
        else:
            CustomSoap_Data['allowCtiControlFlag'] = 'true'

        # Comprobamos si existe la Key shareLineAppearanceCssName
        if 'shareLineAppearanceCssName' in varFORM:
            CustomSoap_Data['shareLineAppearanceCssName'] = varFORM['shareLineAppearanceCssName']

        # Comprobamos si existe la Key callPickupGroupName
        if 'callPickupGroupName' in varFORM:
            CustomSoap_Data['callPickupGroupName'] = varFORM['callPickupGroupName']

        # Comprobamos si existe la Key callForwardAll callingSearchSpaceName
        if 'callForwardAll' in varFORM:
            if 'callingSearchSpaceName' in varFORM:
                CustomSoap_Data['callForwardAll'] = {
                    'destination': '',
                    'forwardToVoiceMail': 'false',
                    'callingSearchSpaceName': varFORM['callingSearchSpaceName'],
                    'secondaryCallingSearchSpaceName': varFORM['callingSearchSpaceName'],
                }
                CustomSoap_Data['callForwardBusy'] = {
                    'destination': '',
                    'forwardToVoiceMail': 'false',
                    'callingSearchSpaceName': varFORM['callingSearchSpaceName'],
                }
            else:
                CustomSoap_Data['callForwardAll'] = {
                    'destination': '',
                    'forwardToVoiceMail': 'false',
                    'callingSearchSpaceName': varFORM['shareLineAppearanceCssName'],
                    'secondaryCallingSearchSpaceName': varFORM['shareLineAppearanceCssName'],
                }
                CustomSoap_Data['callForwardBusy'] = {
                    'destination': '',
                    'forwardToVoiceMail': 'false',
                    'callingSearchSpaceName': varFORM['shareLineAppearanceCssName'],
                }
            CustomSoap_Data['callForwardBusyInt'] = CustomSoap_Data['callForwardBusy']
            CustomSoap_Data['callForwardNoAnswer'] = CustomSoap_Data['callForwardBusy']
            CustomSoap_Data['callForwardNoAnswerInt'] = CustomSoap_Data['callForwardBusy']
            CustomSoap_Data['callForwardNoCoverage'] = CustomSoap_Data['callForwardBusy']
            CustomSoap_Data['callForwardNoCoverageInt'] = CustomSoap_Data['callForwardBusy']
            CustomSoap_Data['callForwardOnFailure'] = CustomSoap_Data['callForwardBusy']
            CustomSoap_Data['callForwardNotRegistered'] = CustomSoap_Data['callForwardBusy']
            CustomSoap_Data['callForwardNotRegisteredInt'] = CustomSoap_Data['callForwardBusy']

        # Replicando el bucle anterior puedo añadir todas las variables que tiene un Directory Number
        try:
            # Damos de alta el Directory Number y no verificamos si existe el mismo Directory Number
            CustomUser_Resp = CustomService.addLine(CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            return {'Class': 'line','AXL': 'add','Method': 'POST', 'Status': 'ERROR', 'Detail': str(sys.exc_info()[1]),'pattern':varFORM['pattern'],'routePartitionName':varFORM['routePartitionName']},400
        else:
            infoLogger.info('Se ha configurado el Translation Pattern %s en la Particion %s' % (varFORM['pattern'],varFORM['routePartitionName']))
            return {'Class': 'line','AXL': 'add','Method': 'POST', 'Status': 'OK', 'Detail': CustomUser_Resp['return'],'pattern':varFORM['pattern'],'routePartitionName':varFORM['routePartitionName']}

    def patch(self):
        # * Funcion para buscar todos los elementos que coincidan con el criterio
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoAXL_Line' )
        return {'Class': 'line','AXL': 'list','Method': 'PATCH', 'Status': 'ERROR', 'Detail': 'No esta definida la funcion'},400

    def put(self):
        # * Funcion para actualizar un elemento
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion put de la clase CiscoAXL_Line' )
        return {'Class': 'line','AXL': 'update','Method': 'PUT', 'Status': 'ERROR', 'Detail': 'No esta definida la funcion'},400

    def delete(self):
        # * Funcion para borrar un Directory Number
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion delete de la clase CiscoAXL_Line' )
        varFORM = request.form
        if all (k in varFORM for k in ('pattern', 'routePartitionName')):
            infoLogger.debug('Esta borrando el Directory Number %s en la Particion %s' % (varFORM['pattern'],varFORM['routePartitionName']))
            CustomSoap_Data = {
                    'pattern': varFORM['pattern'],
                    'routePartitionName': varFORM['routePartitionName']
            }
        else:
            infoLogger.error('No estan todas los parametros requeridos: %s' % (varFORM))
            return {'Class': 'line','AXL': 'remove','Method': 'DELETE', 'Status': 'ERROR', 'Detail': 'Faltan parametros'},400

        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))
        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        try:
            CustomUser_Resp = CustomService.removeTransPattern(**CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            infoLogger.error(type(zeep.helpers.serialize_object(sys.exc_info()[1])))
            return {'Class': 'line','AXL': 'remove','Method': 'DELETE', 'Status': 'ERROR', 'Detail': str(sys.exc_info()[1]),'pattern':varFORM['pattern'],'routePartitionName':varFORM['routePartitionName']},400
        else:
            infoLogger.info('Se ha borrado el Directory Number %s en la Particion %s' % (varFORM['pattern'],varFORM['routePartitionName']))
            return {'Class': 'line','AXL': 'remove','Method': 'DELETE', 'Status': 'OK', 'Detail': str(CustomUser_Resp['return']),'pattern':varFORM['pattern'],'routePartitionName':varFORM['routePartitionName']}

