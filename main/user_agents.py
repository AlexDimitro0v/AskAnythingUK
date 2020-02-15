from django_user_agents.utils import get_user_agent

def get_user_info(request):
    print(get_user_agent(request))

def new_device(request):
    old_info = None
    
