# upload - Flask Cisco Collaboration
Aqui es donde se guardan los ficheros subidos por la Rest API

# Template
La primera línea del fichero contiene el valor de los campos.
## CUCM
### Phone
Los campo que podemos utilizar, porque son los que estan implementado en la funciona CiscoAXL_Line y CiscoAXL_Phone son:

 * FirstName
 * Surname
 * userPrincipalName
 * digestUser
 * pattern
 * routePartitionName
 * shareLineAppearanceCssName
 * callForwardAll
 * callingSearchSpaceName
 * IPPhone
 * name
 * e164Mask
 * devicePoolName
 * commonPhoneConfigName
 * locationName
 * phoneTemplateName

El formato que tenemos que utilizar para dar de alta Translation Pattern es:

```
FirstName,Surname,userPrincipalName,digestUser,pattern,routePartitionName,shareLineAppearanceCssName,callForwardAll,callingSearchSpaceName,IPPhone,name,e164Mask,devicePoolName,commonPhoneConfigName,locationName,phoneTemplateName
Carlos,Sanz,carlos.sanz,,12205,Interna,4_Internacional,,1_Interna,CSF,CSF12205,913236708,Madrid,Axians_Common_Phone_Profile,Madrid,Standard Client Services Framework
```
### User
Los campo que podemos utilizar, porque son los que estan implementado en la funciona CiscoAXL_Line y CiscoAXL_Phone son:

 * userid
 * lastName
 * password
 * telephoneNumber

```
userid,lastName,password,telephoneNumber
2000,Pruebas CSP,2000,2000
```

### TransPattern
Con esta función vamos a poder dar de alta un Translation Pattern.

Los campo que podemos utilizar, porque son los que estan implementado en la funciona CiscoAXL_TransPattern son:

 * pattern
 * routePartitionName
 * description
 * calledPartyTransformationMask
 * callingSearchSpaceName
 * patternUrgency
 * provideOutsideDialtone

El formato que tenemos que utilizar para dar de alta Translation Pattern es:

```
pattern,description,routePartitionName,callingSearchSpaceName,calledPartyTransformationMask
6612204,6612204 - 12204,Interna,1_Interna,12204
```
## CMS
### coSpace
El formato de los archivos que se suben es:

```
name,uri,secondaryUri,callId,cdrTag,defaultlayout,tenant,callProfile,requireCallId
cospace.user01,cospace.user01,500201,500201,cospace.user,allEqual,8b94a144-e6ed-4448-9946-6be3f19fe0f1,442de48f-0a5d-4504-959c-de8a22d23048,true
```