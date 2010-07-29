import os  
from subprocess import PIPE, Popen

class Snmp(object):

    def snmpget(self,host,oid,version="1", community="public"):        
        p = Popen("snmpget -c %s -v %s %s %s" %(community,version,host,oid), shell=True,stdout=PIPE)
        out_, error_ = p.communicate()
        if error_ is None:            
            try:
                return out_.strip().split('=')[1]
            except IndexErrror:
                pass
        return None
        
    def snmpwalk(self,host,oid,version="1", community="public"):
        p = Popen("snmpwalk -c %s -v %s %s %s" %(community,version,host,oid), shell=True, stdout=PIPE)
        out = p.stdout.readlines()
        value = []
        for o in out:      
            try:   
                value.append(o.split('=')[1].strip())   
            except:
                pass
        p.communicate()    
        return value
        
    def snmpset(self,host,oid, valor, version="1", community="public"):
        p = Popen("snmpset -c %s -v %s %s %s %s" %(community,version,host,oid,valor),shell=True,stdout=PIPE)
        out_, erro_ = p.communicate()
        if error_ is None:
            try:
                return out_.split('=')[1].strip()
            except:
                pass 
        return None
