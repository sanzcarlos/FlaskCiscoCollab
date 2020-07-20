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

# *------------------------------------------------------------------
# * Rest API - Cisco AXL - Description
# *
# *  GET    - get    - to retrieve resource representation/information only
# *  PUT    - update - to update existing resource
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

class CiscoAXL_ServiceParameter(Resource):
    def get(self):
        # * Funcion para obtener todos los parametros de un elemento
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion get de la clase CiscoAXL_ServiceParameter' )
        infoLogger.debug('Esta utilizando el metodo GET' )
        varFORM = request.form
        infoLogger.debug('Los datos del formulario son: %s' % (varFORM))
        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))
        infoLogger.debug('Esta buscando el ProcessNode: %s' % (varFORM['name']))
        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        CustomSoap_Data = {
            'processNodeName': varFORM['processNodeName'],
            'name': varFORM['name'],
            'service': varFORM['service']
        }

        try:
            CustomUser_Resp = CustomService.getServiceParameter(**CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            return {'Class': 'ServiceParameter','AXL': 'get','Method': 'GET', 'Status': 'ERROR', 'Detail': str(sys.exc_info()[1]),'name:':varFORM['name']},400
        else:
            return json.loads(json.dumps(zeep.helpers.serialize_object(CustomUser_Resp['return'])))

    def patch(self):
        # * Funcion para buscar todos los elementos que coincidan con el criterio listProcessNode
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion PATCH de la clase CiscoAXL_ServiceParameter' )
        infoLogger.debug('Esta utilizando el metodo PATCH' )
        varFORM = request.form
        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))
        infoLogger.debug('Esta buscando los ServiceParameter con el siguiente criterio: %s - %s' % (varFORM['processNodeName'],varFORM['service']))
        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        searchCriteria = {'processNodeName':varFORM['processNodeName'], 'service':varFORM['service']}
        returnedTags = {'processNodeName':'','name':'','service':'','value':'','valueType':'','uuid':''}

        CustomSoap_Data = {
            'searchCriteria': searchCriteria,
            'returnedTags' : returnedTags,
        }

        try:
            CustomUser_Resp = CustomService.listServiceParameter(**CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            return {'Class': 'ServiceParameter','AXL': 'list','Method': 'PATCH', 'Status': 'ERROR', 'Detail': str(sys.exc_info()[1]),'searchCriteria':varFORM['searchCriteria']},400
        else:
            return json.loads(json.dumps(zeep.helpers.serialize_object(CustomUser_Resp['return'])))


    def put(self):
        # * Funcion para obtener todos los parametros de un elemento
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion PUT de la clase CiscoAXL_ServiceParameter' )
        infoLogger.debug('Esta utilizando el metodo PUT' )
        varFORM = request.form
        infoLogger.debug('Los datos del formulario son: %s' % (varFORM))
        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))
        infoLogger.debug('Esta buscando el ProcessNode: %s' % (varFORM['name']))
        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        CustomSoap_Data = {
            'processNodeName': varFORM['processNodeName'],
            'name': varFORM['name'],
            'service': varFORM['service'],
            'value': varFORM['value']
        }

        try:
            CustomUser_Resp = CustomService.updateServiceParameter(**CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            return {'Class': 'ServiceParameter','AXL': 'update','Method': 'PUT', 'Status': 'ERROR', 'Detail': str(sys.exc_info()[1]),'name:':varFORM['name']},400
        else:
            return {'Class': 'ServiceParameter','AXL': 'update','Method': 'PUT', 'Status': 'OK', 'Detail': CustomUser_Resp['return']},201

