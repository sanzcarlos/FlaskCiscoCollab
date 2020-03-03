# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * cspaxl_RoutePartition.py
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

class CiscoAXL_RoutePartition(Resource):
    def get(self):
        # * Funcion para obtener todos los parametros de un elemento
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion get de la clase CiscoAXL_RoutePartition' )
        return {'Class': 'RoutePartition','AXL': 'get','Method': 'GET', 'Status': 'ERROR', 'Detail': 'No esta definida la funcion'},400

    def post(self):
        # * Funcion para crear un elemento
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoAXL_RoutePartition' )
        return {'Class': 'RoutePartition','AXL': 'add','Method': 'POST', 'Status': 'ERROR', 'Detail': 'No esta definida la funcion'},400

    def patch(self):
        # * Funcion para buscar todos los elementos que coincidan con el criterio
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoAXL_RoutePartition' )
        return {'Class': 'RoutePartition','AXL': 'list','Method': 'PATCH', 'Status': 'ERROR', 'Detail': 'No esta definida la funcion'},400

    def put(self):
        # * Funcion para actualizar un elemento
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion put de la clase CiscoAXL_RoutePartition' )
        return {'Class': 'RoutePartition','AXL': 'update','Method': 'PUT', 'Status': 'ERROR', 'Detail': 'No esta definida la funcion'},400

    def delete(self):
        # * Funcion para borrar un elemento
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion delete de la clase CiscoAXL_RoutePartition' )
        return {'Class': 'RoutePartition','AXL': 'remove','Method': 'DELETE', 'Status': 'ERROR', 'Detail': 'No esta definida la funcion'},400
