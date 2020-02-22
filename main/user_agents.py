from django_user_agents.utils import get_user_agent
from ipware import get_client_ip
from .models import Device, Rating

def save_device_info(request):
    ip, is_routable = get_client_ip(request)
    browser_family = request.user_agent.browser.family
    browser_version = request.user_agent.browser.version_string
    os_family = request.user_agent.os.family
    os_version = request.user_agent.os.version_string
    device_family = request.user_agent.device.family

    prev_devices = Device.objects.filter(user=request.user)

    d = Device(user=request.user,
               ip=ip,
               browser_family=browser_family,
               browser_version=browser_version,
               os_family=os_family,
               os_version=os_version,
               device_family=device_family)

    for device in prev_devices:
        if device == d:
            return

    d.save()
    return d

def check_for_fraud(feedbacker, device):
    rating_feedbackees = Rating.objects.values_list('feedbackee', flat=True).filter(feedbacker=feedbacker)
    devices = Device.objects.filter(user__in=set(rating_feedbackees))

    for d in devices:
        if d.ip == device.ip and d.browser_family == device.browser_family and d.os_family == device.os_family and d.browser_version == device.browser_version and d.os_version == device.os_version and d.user != device.user:
            # Same device suspected
            return True

    # Different device or device config
    return False
