# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * cspaxl_Change.py
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
import sys
import json
import zeep
import logging

class CiscoAXL_Change(Resource):
    def get(self):
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion get de la clase CiscoAXL_Change' )
        return jsonify({'Class': 'Change','AXL': 'Get','Method': 'GET', 'Status': 'Ok'})

    def post(self):
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoAXL_Change' )
        return jsonify({'Class': 'Change','AXL': 'Add','Method': 'POST', 'Status': 'Ok'})

    def patch(self):
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoAXL_Change' )

        CustomService = CustomSoap.ClientSoap (infoLogger,varJSON['mmpHost'],varJSON['mmpUser'],varJSON['mmpPass'],varJSON['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        CustomSoap_Data = {
            'objectList': 'User'
        }

        try:
            #CustomUser_Resp = CustomService.listChange(**CustomSoap_Data)
            CustomUser_Resp = CustomService.listChange()
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            CustomSoap_Data = {
                'Method': 'PATCH',
                'Status': 'Error',
                'Detail': sys.exc_info()[1]
            }
            return jsonify(CustomSoap_Data)
        else:
            #infoLogger.info('Se ha encontrado el Translation Pattern %s en la Particion %s' % (varJSON['varPattern'],varJSON['varroutePartitionName']))
            return json.loads(json.dumps(zeep.helpers.serialize_object(CustomUser_Resp['return'])))


        return jsonify({'Class': 'Change','AXL': 'List','Method': 'PATCH', 'Status': 'Ok'})

    def put(self):
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion put de la clase CiscoAXL_Change' )
        return jsonify({'Class': 'Change','AXL': 'Update','Method': 'PUT', 'Status': 'Ok'})

    def delete(self):
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion delete de la clase CiscoAXL_Change' )
        return jsonify({'Class': 'Change','AXL': 'Remove','Method': 'DELETE', 'Status': 'Ok'})