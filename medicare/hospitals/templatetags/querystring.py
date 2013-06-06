from django.core.exceptions import ImproperlyConfigured
from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def pageless_querystring(context):
    if "request" not in context:
        raise ImproperlyConfigured((
            "The template context does not contain a request object. Please "
            "add the ``django.core.context_processors.request`` context "
            "processor to your ``TEMPLATE_CONTEXT_PROCESSORS`` setting."

        ))
    query_dict = context['request'].GET.copy()
    query_dict.pop("page", None)
    return query_dict.urlencode() + "&"
