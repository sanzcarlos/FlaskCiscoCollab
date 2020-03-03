# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * cspaxl_Phone.py
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

class CiscoAXL_Phone(Resource):
    def get(self):
        # * Funcion para obtener todos los parametros de un elemento
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion get de la clase CiscoAXL_Phone' )
        varFORM = request.form
        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))
        infoLogger.debug('Esta buscando el Phone con el nombre: %s' % (varFORM['name']))
        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        CustomSoap_Data = {
            'name': varFORM['name']
        }

        try:
            CustomUser_Resp = CustomService.getPhone(**CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            return {'Class': 'Phone','AXL': 'get','Method': 'GET', 'Status': 'ERROR', 'Detail': str(sys.exc_info()[1]),'name':varFORM['name']},400
        else:
            # *------------------------------------------------------------------
            # * Tenemos que convertir la variable vendorConfig que es una lista
            # * en un dictionary de tipo string para poder añadirlo a la variable
            # * JSON que tiene que devolver la funcion
            # *------------------------------------------------------------------
            CustomUser_Resp_temp = {}
            for i in range(len(CustomUser_Resp['return']['phone']['vendorConfig']['_value_1'])):
                CustomUser_Resp_temp['_value_'+str(i)] = str(CustomUser_Resp['return']['phone']['vendorConfig']['_value_1'][i])
            CustomUser_Resp['return']['phone']['vendorConfig']['_value_1'] = CustomUser_Resp_temp
            return json.loads(json.dumps(zeep.helpers.serialize_object(CustomUser_Resp['return'])))

    def post(self):
        # * Funcion para crear un phone
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoAXL_Phone' )
        varFORM = request.form
        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))

        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        CustomSoap_Data = {}

        # Comprobamos si existe las siguientes Key's name, product, class, protocol, protocolSide, devicePoolName, commonPhoneConfigName, locationName, useTrustedRelayPoint, phoneTemplateName, primaryPhoneName, builtInBridgeStatus, packetCaptureMode, certificateOperation and deviceMobilityMode
        if all (k in varFORM for k in ('name', 'product', 'class', 'protocol', 'protocolSide', 'devicePoolName', 'commonPhoneConfigName', 'locationName', 'useTrustedRelayPoint', 'phoneTemplateName', 'primaryPhoneName', 'builtInBridgeStatus', 'packetCaptureMode', 'certificateOperation', 'deviceMobilityMode')):
            infoLogger.debug('Se quiere dar de alta un telefono con el nombre %s modelo %s' % (varFORM['name'],varFORM['product']))
            CustomSoap_Data['name'] = varFORM['name']
            CustomSoap_Data['product'] = varFORM['product']
            CustomSoap_Data['class'] = varFORM['class']
            CustomSoap_Data['protocol'] = varFORM['protocol']
            CustomSoap_Data['protocolSide'] = varFORM['protocolSide']
            CustomSoap_Data['devicePoolName'] = varFORM['devicePoolName']
            CustomSoap_Data['commonPhoneConfigName'] = varFORM['commonPhoneConfigName']
            CustomSoap_Data['locationName'] = varFORM['locationName']
            CustomSoap_Data['useTrustedRelayPoint'] = varFORM['useTrustedRelayPoint']
            CustomSoap_Data['phoneTemplateName'] = varFORM['phoneTemplateName']
            CustomSoap_Data['builtInBridgeStatus'] = varFORM['builtInBridgeStatus']
            CustomSoap_Data['packetCaptureMode'] = varFORM['packetCaptureMode']
            CustomSoap_Data['certificateOperation'] = varFORM['certificateOperation']
            CustomSoap_Data['deviceMobilityMode'] = varFORM['deviceMobilityMode']
        else:
            infoLogger.error('No estan todas los parametros requeridos: %s' % (varFORM))
            return {'Class': 'Phone','AXL': 'add','Method': 'POST', 'Status': 'ERROR', 'Detail': 'Faltan parametros'},400
        
        # Comprobamos si existe la Key description
        if 'description' in varFORM:
            CustomSoap_Data['description'] = varFORM['description']
        # Comprobamos si existe la Key ownerUserName
        if 'ownerUserName' in varFORM:
            CustomSoap_Data['ownerUserName'] = varFORM['ownerUserName']
            # Comprobamos si existe la Key digestUser
            if 'digestUser' in varFORM:
                CustomSoap_Data['digestUser'] = varFORM['digestUser']
            else:
                CustomSoap_Data['digestUser'] = varFORM['ownerUserName']
        # Comprobamos si existe la Key subscribeCallingSearchSpaceName
        if 'subscribeCallingSearchSpaceName' in varFORM:
            CustomSoap_Data['subscribeCallingSearchSpaceName'] = varFORM['subscribeCallingSearchSpaceName']
        # Comprobamos si existe la Key lines
        if all (k in varFORM for k in ('lines', 'routePartitionName', 'e164Mask')):
            if 'ownerUserName' in varFORM:
                CustomSoap_Data['lines'] = {
                    'line':{
                        'index': 1,
                        'display': varFORM['lines'] + ' ' + varFORM['description'],
                        'e164Mask': varFORM['e164Mask'],
                        'label': varFORM['lines'] + ' ' + varFORM['description'],
                        'dirn': {
                            'pattern': varFORM['lines'],
                            'routePartitionName': varFORM['routePartitionName'],
                        },
                        'associatedEndusers': {
                            'enduser':{
                                'userId': varFORM['ownerUserName'],
                            },
                        },
                        'maxNumCalls': 6,
                        'busyTrigger': 2,
                    },
                }
            else:
                CustomSoap_Data['lines'] = {
                    'line':{
                        'index': 1,
                        'display': varFORM['lines'] + ' ' + varFORM['description'],
                        'e164Mask': varFORM['e164Mask'],
                        'label': varFORM['lines'] + ' ' + varFORM['description'],
                        'dirn': {
                            'pattern': varFORM['lines'],
                            'routePartitionName': varFORM['routePartitionName'],
                        },
                        'maxNumCalls': 6,
                        'busyTrigger': 2,
                    },
                }

        try:
            # Damos de alta el telefono y no verificamos si existe el mismo telefono
            CustomUser_Resp = CustomService.addPhone(CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            return jsonify({'Class': 'Phone','AXL': 'add','Method': 'POST', 'Status': 'ERROR', 'Detail': str(sys.exc_info()[1]),'name':varFORM['name'], 'product': varFORM['product']})
        else:
            infoLogger.info('Se ha configurado el telefono %s' % (varFORM['name']))
            return jsonify({'Class': 'Phone','AXL': 'add','Method': 'POST', 'Status': 'OK', 'Detail': str(CustomUser_Resp['return']),'name':varFORM['name'], 'product': varFORM['product']})


        return {'Class': 'Phone','AXL': 'add','Method': 'POST', 'Status': 'ERROR', 'Detail': 'No esta definida la funcion'},400

    def patch(self):
        # * Funcion para buscar todos los elementos que coincidan con el criterio
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoAXL_Phone' )
        return {'Class': 'Phone','AXL': 'list','Method': 'PATCH', 'Status': 'ERROR', 'Detail': 'No esta definida la funcion'},400

    def put(self):
        # * Funcion para actualizar un elemento
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion put de la clase CiscoAXL_Phone' )
        return {'Class': 'Phone','AXL': 'update','Method': 'PUT', 'Status': 'ERROR', 'Detail': 'No esta definida la funcion'},400

    def delete(self):
        # * Funcion para borrar un telefono
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion delete de la clase CiscoAXL_Phone' )
        varFORM = request.form
        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))
        infoLogger.debug('Vamos a borrar el Phone con el nombre: %s' % (varFORM['name']))
        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        CustomSoap_Data = {
            'name': varFORM['name']
        }

        try:
            CustomUser_Resp = CustomService.removePhone(**CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            return {'Class': 'Phone','AXL': 'remove','Method': 'DELETE', 'Status': 'ERROR', 'Detail': str(sys.exc_info()[1]),'name':varFORM['name']},400
        else:
            # *------------------------------------------------------------------
            # * Tenemos que convertir la variable vendorConfig que es una lista
            # * en un dictionary de tipo string para poder añadirlo a la variable
            # * JSON que tiene que devolver la funcion
            # *------------------------------------------------------------------
            return {'Class': 'Phone','AXL': 'remove','Method': 'DELETE', 'Status': 'OK', 'Detail': str(CustomUser_Resp['return']),'name':varFORM['name']}
