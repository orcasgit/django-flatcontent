from django import template

from flatcontent.models import FlatContent

register = template.Library()

class FlatContentNode(template.Node):
    def __init__(self, slug, context_var=None):
        self.slug = slug
        self.context_var = context_var

    def render(self, context):
        if not self.context_var:
            return FlatContent.get(slug=self.slug)
        else:
            context[self.context_var] = FlatContent.get(slug=self.slug)
        return ''

def do_flatcontent(parser, token):
    """
    Retrieves content from the ``FlatContent`` model given a slug, and
    optionally stores it in a context variable.
    
    Usage::
    
        {% flatcontent [slug] %}
    
    Or to get the flatcontent into a variable for later use in the template or
    with tags and filters::
    
        {% flatcontent [slug] as [varname] %}
    
    """
    bits = token.split_contents()
    len_bits = len(bits)
    varname = None
    if len_bits not in (2, 4):
        raise template.TemplateSyntaxError, "The flatcontent tag requires either 1 or 3 arguments"
    if len_bits == 2:
        return FlatContentNode(bits[1])
    elif len_bits == 4:
        if bits[2] != 'as':
            raise TemplateSyntaxError("The second argument to flatcontent tag must be 'as'")
        return FlatContentNode(bits[1], bits[3])

register.tag('flatcontent', do_flatcontent)
