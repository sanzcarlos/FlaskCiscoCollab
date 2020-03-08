# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * cspaxl_CallPickupGroup.py
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

class CiscoAXL_CallPickupGroup(Resource):
    def get(self):
        # * Funcion para obtener todos los datos de un Call Pickup Group
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion get de la clase CiscoAXL_CallPickupGroup' )
        varFORM = request.form
        if 'name' in varFORM:
            infoLogger.debug('Esta buscando el Call PickUp Group %s' % (varFORM['name']))
            CustomSoap_Data = {
                    'name': varFORM['name'],
            }
        else:
            infoLogger.error('No estan todas los parametros requeridos: %s' % (varFORM))
            return {'Class': 'CallPickupGroup','AXL': 'get','Method': 'GET', 'Status': 'ERROR', 'Detail': 'Faltan parametros'},400

        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))
        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        try:
            CustomUser_Resp = CustomService.getCallPickupGroup(**CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            infoLogger.error(type(zeep.helpers.serialize_object(sys.exc_info()[1])))
            return {'Class': 'CallPickupGroup','AXL': 'get','Method': 'GET', 'Status': 'ERROR', 'Detail': str(sys.exc_info()[1]),'name':varFORM['name']},400
        else:
            infoLogger.info('Se ha encontrado el Call Pickup Group %s' % (varFORM['name']))
            return json.loads(json.dumps(zeep.helpers.serialize_object(CustomUser_Resp['return'])))

    def post(self):
        # * Funcion para crear un Call Pickup Group
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoAXL_CallPickupGroup' )
        varFORM = request.form
        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))
        if all (k in varFORM for k in ('pattern', 'name', 'routePartitionName')):
            infoLogger.debug('Se quiere dar de alta el Call Pickup Group %s en la Particion %s' % (varFORM['pattern'],varFORM['routePartitionName']))
            CustomSoap_Data = {
                    'pattern': varFORM['pattern'],
                    'name': varFORM['name'],
                    'routePartitionName': varFORM['routePartitionName']
            }
        else:
            infoLogger.error('No estan todas los parametros requeridos: %s' % (varFORM))
            return {'Class': 'CallPickupGroup','AXL': 'add','Method': 'POST', 'Status': 'ERROR', 'Detail': 'Faltan parametros'},400

        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        # Comprobamos si existe la Key description
        if 'description' in varFORM:
            CustomSoap_Data['description'] = varFORM['description']

        # Comprobamos si existe la Key pickupNotification
        if 'pickupNotification' in varFORM:
            CustomSoap_Data['pickupNotification'] = varFORM['pickupNotification']
            # Comprobamos si existe la Key callInfoForPickupNotification
            if 'callInfoForPickupNotification' in varFORM:
                CustomSoap_Data['callInfoForPickupNotification'] = {
                    'callingPartyInfo': varFORM['callInfoForPickupNotification'],
                    'calledPartyInfo': varFORM['callInfoForPickupNotification'],
                }

        # Comprobamos si existe la Key pickupNotificationTimer
        if 'pickupNotificationTimer' in varFORM:
            CustomSoap_Data['pickupNotificationTimer'] = varFORM['pickupNotificationTimer']

        # Replicando el bucle anterior puedo añadir todas las variables que tiene un Call Pickup Group
        try:
            # Damos de alta el Call Pickup Group y no verificamos si existe el mismo Call Pickup Group
            CustomUser_Resp = CustomService.addCallPickupGroup(CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            return {'Class': 'CallPickupGroup','AXL': 'add','Method': 'POST', 'Status': 'ERROR', 'Detail': str(sys.exc_info()[1]),'pattern':varFORM['pattern'],'routePartitionName':varFORM['routePartitionName'],'name':varFORM['name']},400
        else:
            infoLogger.info('Se ha configurado el Call Pickup Group %s en la Particion %s' % (varFORM['pattern'],varFORM['routePartitionName']))
            return {'Class': 'CallPickupGroup','AXL': 'add','Method': 'POST', 'Status': 'OK', 'Detail': str(sys.exc_info()[1]),'pattern':varFORM['pattern'],'routePartitionName':varFORM['routePartitionName'],'name':varFORM['name']},400

    def patch(self):
        # * Funcion para buscar todos los elementos que coincidan con el criterio
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoAXL_Template' )
        return {'Class': 'CallPickupGroup','AXL': 'list','Method': 'PATCH', 'Status': 'ERROR', 'Detail': 'No esta definida la funcion'},400

    def put(self):
        # * Funcion para actualizar un elemento
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion put de la clase CiscoAXL_Template' )
        return {'Class': 'CallPickupGroup','AXL': 'update','Method': 'PUT', 'Status': 'ERROR', 'Detail': 'No esta definida la funcion'},400

    def delete(self):
        # * Funcion para Borrar el Call Pickup Group
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion get de la clase CiscoAXL_CallPickupGroup' )
        varFORM = request.form
        if 'name' in varFORM:
            infoLogger.debug('Esta borrando el Call PickUp Group %s' % (varFORM['name']))
            CustomSoap_Data = {
                    'name': varFORM['name'],
            }
        else:
            infoLogger.error('No estan todas los parametros requeridos: %s' % (varFORM))
            return {'Class': 'CallPickupGroup','AXL': 'remove','Method': 'DELETE', 'Status': 'ERROR', 'Detail': 'Faltan parametros'},400

        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))
        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        try:
            CustomUser_Resp = CustomService.removeCallPickupGroup(**CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            infoLogger.error(type(zeep.helpers.serialize_object(sys.exc_info()[1])))
            return {'Class': 'CallPickupGroup','AXL': 'remove','Method': 'DELETE', 'Status': 'ERROR', 'Detail': str(sys.exc_info()[1]),'name':varFORM['name']},400
        else:
            infoLogger.info('Se ha encontrado el Call Pickup Group %s' % (varFORM['name']))
            return {'Class': 'CallPickupGroup','AXL': 'remove','Method': 'DELETE', 'Status': 'OK', 'Detail': str(CustomUser_Resp['return']),'name':varFORM['name']}
