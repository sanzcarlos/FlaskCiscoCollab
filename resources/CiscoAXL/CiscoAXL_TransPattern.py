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
        varJSON = request.get_json()
        infoLogger.debug('El cliente es: %s' % (varJSON['Customer']))
        infoLogger.debug('La direccion IP es: %s' % (varJSON['mmpHost']))
        infoLogger.debug('Esta buscando el Translation Pattern %s en la Particion %s' % (varJSON['varPattern'],varJSON['varroutePartitionName']))
        CustomService = CustomSoap.ClientSoap (infoLogger,varJSON['mmpHost'],varJSON['mmpUser'],varJSON['mmpPass'],varJSON['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        CustomSoap_Data = {
            'pattern': varJSON['varPattern'],
            'routePartitionName': varJSON['varroutePartitionName']
        }

        try:
            CustomUser_Resp = CustomService.getTransPattern(**CustomSoap_Data)
        except:
            infoLogger.error('Se ha producido un error en la consulta SOAP')
            infoLogger.debug(sys.exc_info())
            infoLogger.error(sys.exc_info()[1])
            CustomSoap_Data = {
                'Method': 'GET',
                'Status': 'Error',
                'Detail': sys.exc_info()[1]
            }
            return jsonify(CustomSoap_Data)
        else:
            infoLogger.info('Se ha encontrado el Translation Pattern %s en la Particion %s' % (varJSON['varPattern'],varJSON['varroutePartitionName']))
            return json.loads(json.dumps(zeep.helpers.serialize_object(CustomUser_Resp['return'])))

    def post(self):
        # * Funcion para crear un Translation Pattern
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoAXL_TransPattern' )
        return jsonify({'Class': 'TransPattern','AXL': 'Add','Method': 'POST', 'Status': 'Ok'})

    def patch(self):
        # * Funcion para list un Translation Pattern
        infoLogger = logging.getLogger('FlaskCiscoCollab')
        infoLogger.debug('Ha accedido a la funcion post de la clase CiscoAXL_TransPattern' )
        varJSON = request.get_json()
        infoLogger.debug('El cliente es: %s' % (varJSON['Customer']))
        infoLogger.debug('La direccion IP es: %s' % (varJSON['mmpHost']))
        infoLogger.debug('Esta buscando los Translation Pattern con el siguiente criterio: %s' % (varJSON['varsearchCriteria']))
        CustomService = CustomSoap.ClientSoap (infoLogger,varJSON['mmpHost'],varJSON['mmpUser'],varJSON['mmpPass'],varJSON['mmpVersion'])
        CustomService = CustomService.CustomSoapClient ()

        varsearchCriteria = {'pattern':'%' + varJSON['varsearchCriteria'] + '%'}
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