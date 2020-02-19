# -*- coding: iso-8859-15 -*-

# *------------------------------------------------------------------
# * cspaxl_User.py
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

class CiscoAXL_TransPattern(Resource):
    def get(self):
        # * Funcion para obtener todos los datos de un Translation Pattern
        infoLogger = logging.getLogger('FlaskCiscoCollab')

        infoLogger.debug('Ha accedido a la funcion get de la clase CiscoAXL_TransPattern' )
        varFORM = request.form
        # infoLogger.debug('Los datos del formulario son: %s' % (varFORM))
        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))
        infoLogger.debug('Esta buscando el Translation Pattern %s en la Particion %s' % (varFORM['varpattern'],varFORM['varroutePartitionName']))
        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        CustomSoap_Data = {
            'pattern': varFORM['varpattern'],
            'routePartitionName': varFORM['varroutePartitionName']
        }

        try:
            CustomUser_Resp = CustomService.getTransPattern(**CustomSoap_Data)
            #CustomUser_Resp = CustomService.getTransPattern(CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            infoLogger.error(type(zeep.helpers.serialize_object(sys.exc_info()[1])))
            return jsonify({'Class': 'TransPattern','AXL': 'get','Method': 'GET', 'Status': 'ERROR', 'Detail': str(sys.exc_info()[1]),'pattern':varFORM['pattern'], 'routePartitionName': varFORM['routePartitionName']})
        else:
            infoLogger.info('Se ha encontrado el Translation Pattern %s en la Particion %s' % (varFORM['varpattern'],varFORM['varroutePartitionName']))
            return json.loads(json.dumps(zeep.helpers.serialize_object(CustomUser_Resp['return'])))

    def post(self):
        # * Funcion para crear un Translation Pattern
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoAXL_TransPattern' )
        varFORM = request.form
        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))
        infoLogger.debug('Se quiere dar de alta el Translation Pattern %s en la Particion %s' % (varFORM['pattern'],varFORM['routePartitionName']))

        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        CustomSoap_Data = {}

        # Comprobamos si el Pattern tiene el caracter +
        if varFORM['pattern'][0] == '+':
            CustomSoap_Data['pattern'] = '\\' + varFORM['pattern']
        else:
            CustomSoap_Data['pattern'] = varFORM['pattern']
        CustomSoap_Data['usage'] = 'Translation'
        CustomSoap_Data['routePartitionName'] = varFORM['routePartitionName']
        # Comprobamos si existe la Key description
        if 'description' in varFORM:
            CustomSoap_Data['description'] = varFORM['description']
        else:
            # Comprobamos si existe la Key CalledPartyTransformMask
            if 'calledPartyTransformationMask' in varFORM:
                CustomSoap_Data['description'] = varFORM['pattern'] + ' - ' + varFORM['calledPartyTransformationMask']
                CustomSoap_Data['calledPartyTransformationMask'] = varFORM['calledPartyTransformationMask']
            else:
                CustomSoap_Data['description'] = varFORM['pattern']
        # Comprobamos si existe la Key callingSearchSpaceName
        if 'callingSearchSpaceName' in varFORM:
            CustomSoap_Data['callingSearchSpaceName'] = varFORM['callingSearchSpaceName']
        # Comprobamos si existe la Key patternUrgency
        if 'patternUrgency' in varFORM:
            CustomSoap_Data['patternUrgency'] = varFORM['patternUrgency']
        else:
            CustomSoap_Data['patternUrgency'] = 'true'
        # Comprobamos si existe la Key provideOutsideDialtone
        if 'provideOutsideDialtone' in varFORM:
            CustomSoap_Data['provideOutsideDialtone'] = varFORM['provideOutsideDialtone']
        else:
            CustomSoap_Data['provideOutsideDialtone'] = 'false'
        # Replicando el bucle anterior puedo añadir todas las variables que tiene el Translation Pattern
        try:
            # Damos de alta el translation Pattern y no verificamos si existe el mismo translation Pattern
            CustomUser_Resp = CustomService.addTransPattern(CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            return jsonify({'Class': 'TransPattern','AXL': 'add','Method': 'POST', 'Status': 'ERROR', 'Detail': str(sys.exc_info()[1]),'pattern':varFORM['pattern'], 'routePartitionName': varFORM['routePartitionName']})
        else:
            infoLogger.info('Se ha configurado el Translation Pattern %s en la Particion %s' % (varFORM['pattern'],varFORM['routePartitionName']))
            return json.loads(json.dumps(zeep.helpers.serialize_object(CustomUser_Resp['return'])))

    def patch(self):
        # * Funcion para list un Translation Pattern
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoAXL_TransPattern' )
        varFORM = request.form
        infoLogger.debug('Los datos del formulario son: %s' % (varFORM))
        infoLogger.debug('La direccion IP es: %s' % (varFORM['mmpHost']))
        infoLogger.debug('Esta buscando los Translation Pattern con el siguiente criterio: %s' % (varFORM['varsearchCriteria']))
        CustomService = CustomSoap.ClientSoap (infoLogger,varFORM['mmpHost'],varFORM['mmpUser'],varFORM['mmpPass'],varFORM['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        varsearchCriteria = {'pattern':'%' + varFORM['varsearchCriteria'] + '%'}
        varreturnedTags = {'pattern':'','description':'','usage':'','routePartitionName':'','blockEnable':'','calledPartyTransformationMask':'','callingPartyTransformationMask':'','useCallingPartyPhoneMask':'','callingPartyPrefixDigits':'','dialPlanName':'','digitDiscardInstructionName':'','patternUrgency':'','prefixDigitsOut':'','routeFilterName':'','callingLinePresentationBit':'','callingNamePresentationBit':'','connectedLinePresentationBit':'','connectedNamePresentationBit':'','patternPrecedence':'','provideOutsideDialtone':'','callingPartyNumberingPlan':'','callingPartyNumberType':'','calledPartyNumberingPlan':'','calledPartyNumberType':'','callingSearchSpaceName':'','resourcePriorityNamespaceName':'','routeNextHopByCgpn':'','routeClass':'','callInterceptProfileName':'','releaseClause':'','useOriginatorCss':'','dontWaitForIDTOnSubsequentHops':'','isEmergencyServiceNumber':''}

        CustomSoap_Data = {
            'searchCriteria': varsearchCriteria,
            'returnedTags' : varreturnedTags,
        }

        try:
            CustomUser_Resp = CustomService.listTransPattern(**CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            sys.exit()
        else:
            return json.loads(json.dumps(zeep.helpers.serialize_object(CustomUser_Resp['return'])))

    def put(self):
        # * Funcion para actualizar un Translation Pattern
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion put de la clase CiscoAXL_TransPattern' )
        return jsonify({'Class': 'TransPattern','AXL': 'Update','Method': 'PUT', 'Status': 'Ok'})

    def delete(self):
        # * Funcion para borrar un Translation Pattern
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion delete de la clase CiscoAXL_TransPattern' )
        return jsonify({'Class': 'TransPattern','AXL': 'Remove','Method': 'DELETE', 'Status': 'Ok'})