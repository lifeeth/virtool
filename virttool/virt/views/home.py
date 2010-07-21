from base import * 
from django.utils.translation import ugettext as _
from django.contrib.auth import logout

def index(request):      
    return render_to_response('virt/index.html',{}, context_instance=RequestContext(request))
    
def logout_view(request):
    logout(request)    
    return HttpResponseRedirect(reverse('home'))
