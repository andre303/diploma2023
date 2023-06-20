from django import template
register = template.Library()
from  trips.models import Guide,SavedGuides
@register.simple_tag
def isSaved(guide, user):
    if user.is_authenticated:
        item = SavedGuides.objects.filter(user = user).first()
        if item:
            return item.guides.filter(pk = guide.pk).exists()
    return False