from django import template

from flatcontent.models import FlatContent

register = template.Library()

class FlatContentNode(template.Node):
    def __init__(self, slug, context_var=None, site_id=None):
        self.slug = slug
        self.context_var = context_var
        self.site_id = site_id

    def render(self, context):
        site_id = self.site_id
        if self.site_id != None:
            site_id = template.Variable(site_id).resolve(context)

        flat_content = FlatContent.get(slug=self.slug, site_id=site_id)
        if not self.context_var:
            return flat_content
        else:
            context[self.context_var] = flat_content
        return ''

def do_flatcontent(parser, token):
    """
    Retrieves content from the ``FlatContent`` model given a slug, and
    optionally stores it in a context variable.
    
    Usage::
    
        {% flatcontent [slug] %}
    
    Optionally, you can specify a site using the following syntax::

        {% flatcontent [slug] for-site [site-id] %}

    To get the flatcontent into a variable for later use in the template or
    with tags and filters::
    
        {% flatcontent [slug] as [varname] %}
    
    """
    bits = token.split_contents()
    len_bits = len(bits)
    varname = None
    if len_bits not in (2, 4, 6):
        raise template.TemplateSyntaxError("The flatcontent tag requires "
                                           "1, 3, or 5 arguments")

    try:
        site_id = bits[bits.index('for-site') + 1]
    except ValueError:
        site_id = None

    try:
        context_var = bits[bits.index('as') + 1]
    except ValueError:
        context_var = None

    if len_bits > 2 and site_id is None and context_var is None:
        raise template.TemplateSyntaxError("The second or fourth argument "
                                           "should be 'as' or 'for-site'")

    return FlatContentNode(bits[1], context_var=context_var, site_id=site_id)

register.tag('flatcontent', do_flatcontent)
