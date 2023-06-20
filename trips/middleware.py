from .models import SiteSettings


class SettingsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        items = SiteSettings.objects.filter(active=True)
        if items:
            request.settings = items[0]
        else:
            request.settings = {
                "title": "Go to Admin -> create active site settings",
                "default_language": "en",
                "slogan": "Setup your site please!",
                "main_text": "",
                "get_language_from_user": True,
                "meta_keywords": "",
                "meta_description": "",
            }
        return self.get_response(request)
