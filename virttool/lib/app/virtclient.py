def getvirttoolservice():
    from pyamf.remoting.client import RemotingService
    from django.conf import settings
    client_ = RemotingService('https://localhost:8789')
    client_.setCredentials("admin", settings.DAEMON_PASSWORD)
    return client_.getService('VirtToolService')

def live_migrate(domainid, nodeid): 
    try:   
        message = getvirttoolservice().live_migrate(domainid, nodeid)
        return message
    except Exception, e:
        return e
        