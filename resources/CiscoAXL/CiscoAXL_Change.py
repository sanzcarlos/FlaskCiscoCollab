# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * cspaxl_Change.py
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

class CiscoAXL_Change(Resource):
    def patch(self):
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoAXL_Change' )
        infoLogger.debug('Esta utilizando el metodo PATCH' )
        varFORM = request.form
        infoLogger.debug('Los datos del formulario son: %s' % (varFORM))
        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))

        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        try:
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
            #infoLogger.debug('Los datos devueltos son: %s' % (CustomUser_Resp))
            return json.loads(json.dumps(zeep.helpers.serialize_object(CustomUser_Resp)))
