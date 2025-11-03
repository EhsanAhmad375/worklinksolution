from .models import SiteSetting


def site_settings(request):
    """Make site settings available to all templates"""
    try:
        settings = SiteSetting.objects.get(pk=1)
    except SiteSetting.DoesNotExist:
        settings = SiteSetting.objects.create()
    return {'site_settings': settings}

