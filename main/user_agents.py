from django_user_agents.utils import get_user_agent

def get_user_info(request):
    print(get_user_agent(request))

    print(request.user_agent.browser.family)  # returns 'Mobile Safari'
    print(request.user_agent.browser.version)  # returns (5, 1)

    print(request.user_agent.os.family)  # returns 'iOS'
    print(request.user_agent.os.version)  # returns (5, 1)

    print(request.user_agent.device)  # returns Device(family='iPhone')
    print(request.user_agent.device.family)  # returns 'iPhone'

def new_device(request):
    old_info = None
