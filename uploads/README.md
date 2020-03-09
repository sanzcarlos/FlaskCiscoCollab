# upload - Flask Cisco Collaboration
Aqui es donde se guardan los ficheros subidos por la Rest API

# Template
## CUCM
### TransPattern
El formato de los archivos que se suben es:

```
pattern,routePartitionName,callingSearchSpaceName,calledPartyTransformationMask
6612204,Interna,1_Interna,12204
```
## CMS
### coSpace
El formato de los archivos que se suben es:

```
name,uri,secondaryUri,callId,cdrTag,defaultlayout,tenant,callProfile,requireCallId
cospace.user01,cospace.user01,500201,500201,cospace.user,allEqual,8b94a144-e6ed-4448-9946-6be3f19fe0f1,442de48f-0a5d-4504-959c-de8a22d23048,true
```