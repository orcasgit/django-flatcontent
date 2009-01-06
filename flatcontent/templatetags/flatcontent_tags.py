from django import template

from flatcontent.models import FlatContent

register = template.Library()

class FlatContentNode(template.Node):
    def __init__(self, slug):
        self.slug = slug

    def render(self, context):
        try:
            fc = FlatContent.objects.get(slug=self.slug)
        except FlatContent.DoesNotExist:
            return ''
        return fc.content

def do_flatcontent(parser, token):
    """
    Retrieves content from the FlatContent model given a slug.
    
    Usage::
    
        {% flatcontent slug %}
    
    """
    try:
        tag_name, slug = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "The flatcontent tag requires exactly one argument"
    return FlatContentNode(slug)

register.tag('flatcontent', do_flatcontent)
