from lxml import etree

from zeep import Client, Settings, Plugin, xsd
from zeep.transports import Transport
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault

from requests import Session
from requests.auth import HTTPBasicAuth

import os
import platform
import urllib3

class ClientSoap (object):
    def __init__ (self,infoLogger,CustomSoapIP,CustomSoapUsername,CustomSoapPassword,CustomSoapVersion='7.0',CustomSoapPort='8443'):
        self.Logger = infoLogger
        self.ipaddress = CustomSoapIP
        self.username = CustomSoapUsername
        self.password = CustomSoapPassword
        self.port = CustomSoapPort
        self.version = CustomSoapVersion
        self.Logger.debug ('Ha accedido a la funcion __init__ de la clase ClientSoap')

    #def Test (self,infoLogger,CustomSoapIP,CustomSoapUsername,CustomSoapPassword,CustomSoapVersion='7.0',CustomSoapPort='8443'):
    def CustomSoapClient (self):
        self.Logger.debug('La direccion IP para la conexion SOAP es: %s' % (self.ipaddress))

        # Comprobamos el SO sobre el que esta funcionando el servidor de Flask
        if platform.system() == 'Windows':
            self.Logger.debug('El sistema operativo es: %s' % (platform.system()))
            CustomWSDL = 'file://' + os.getcwd().replace ("\\","//") + '//Schema//CUCM//' + self.version + '//AXLAPI.wsdl'
        else:
            self.Logger.debug('El sistema operativo es: %s' % (platform.system()))
            CustomWSDL = 'file://' + os.getcwd() + '/Schema/CUCM/' + self.version + '/AXLAPI.wsdl'
        
        self.Logger.debug('El archivo WSDL es: %s' % (CustomWSDL))

        # Definimos la URL de AXL
        self.location = 'https://' + self.ipaddress + ':' + self.port + '/axl/'

        # History shows http_headers
        global CustomHistory
        CustomHistory = HistoryPlugin()

        # The first step is to create a SOAP client session
        CustomSession = Session()

        # We avoid certificate verification by default, but you can uncomment and set
        # your certificate here, and comment out the False setting
        #session.verify = CERT
        CustomSession.verify = False
        CustomSession.auth = HTTPBasicAuth(self.username, self.password)

        CustomTransport = Transport(session=CustomSession, timeout=10, cache=SqliteCache())

        urllib3.disable_warnings()

        # strict=False is not always necessary, but it allows zeep to parse imperfect XML
        CustomSettings = Settings(strict=False, xml_huge_tree=True)

        try:
            CustomSOAPClient = Client(CustomWSDL,
                                        settings=CustomSettings,
                                        transport=CustomTransport,
                                        plugins=[MyLoggingPlugin(),CustomHistory],
            )

            CustomService = CustomSOAPClient.create_service("{http://www.cisco.com/AXLAPIService/}AXLAPIBinding", self.location)
        except:
            self.Logger.error('Se ha producido un error al crear el cliente SOAP')
            self.Logger.debug(sys.exc_info())
            self.Logger.error(sys.exc_info()[1])
            sys.exit()
        else:
            self.Logger.info('Se ha creado el cliente SOAP')
            return (CustomService)

# This class lets you view the incoming and outgoing http headers and/or XML
class MyLoggingPlugin(Plugin):
    def ingress(self, envelope, http_headers, operation):
        print(etree.tostring(envelope, pretty_print=True))
        return envelope, http_headers
    
    def egress(self, envelope, http_headers, operation, binding_options):
        print(etree.tostring(envelope, pretty_print=True))
        return envelope, http_headers