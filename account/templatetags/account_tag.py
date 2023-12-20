from django import template

register = template.Library()


@register.inclusion_tag('partials/_admin_sidebar_link.html')
def link(request, link_name, content, classes, thing=""):
    return {
        "request": request,
        "link_name": link_name,
        "link": "account:{}".format(link_name),
        "content": content,
        "classes": classes,
        "thing": thing,
    }
