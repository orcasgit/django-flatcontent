from django import template

from flatcontent.models import FlatContent

register = template.Library()

class FlatContentNode(template.Node):
    errors = {
        'for-site': {
            'missing': "The argument after 'for-site' should be a site",
        },
        'as': {
            'missing': (
                "The argument after 'as' should be a name for the context var"
            ),
        },
        'with': {
            'missing': "You must include key=value pairs after 'with'",
        }
    }

    def __init__(self, slug, as_=None, for_site=None, with_=None):
        self.slug = slug
        self.as_ = as_
        self.for_site = for_site
        self.with_ = with_ or {}

    def render(self, context):
        site_id = self.for_site
        if self.for_site != None:
            site_id = template.Variable(site_id).resolve(context)

        flat_content = FlatContent.get(
            slug=self.slug,
            site_id=site_id,
            context={
                key: val.resolve(context)
                for key, val in self.with_.items()
            },
        )
        if not self.as_:
            return flat_content
        else:
            context[self.as_] = flat_content
        return ''

def do_flatcontent(parser, token):
    """
    Retrieves content from the ``FlatContent`` model given a slug, and
    optionally stores it in a context variable or adds context.

    Usage::

        {% flatcontent [slug] %}

    Optionally, you can specify a site using the following syntax::

        {% flatcontent [slug] for-site [site-id] %}

    To get the flatcontent into a variable for later use in the template or
    with tags and filters::

        {% flatcontent [slug] as [varname] %}

    To add context for use in flatcontent templates, use `with`::

        {% flatcontent [slug] with [contextvar1]=[contextval1] [contextvar2]=[contextval2] ... %}

    """
    bits = token.split_contents()[1:]
    if len(bits) in (0, 2):
        raise template.TemplateSyntaxError(
            "The flatcontent tag requires 1 or 3+ arguments")

    slug = bits.pop(0)

    kwargs = {}
    kwarg_map = {'for_site': 'for-site', 'as_': 'as', 'with_': 'with'}
    for kwarg, bit in kwarg_map.items():
        try:
            bit_idx = bits.index(bit)
            bits.remove(bit)
            if kwarg == 'with_':
                kwargs[kwarg] = [b.split('=') for b in bits[bit_idx:]]
                if kwargs[kwarg]:
                    kwargs['with_'] = {
                        warg[0]: parser.compile_filter(warg[1])
                        for warg in kwargs['with_']
                    }
                    bits = []
                else:
                    raise IndexError()
            else:
                kwargs[kwarg] = bits.pop(bit_idx)
        except ValueError:
            kwargs[kwarg] = None
        except IndexError:
            raise template.TemplateSyntaxError(
                FlatContentNode.errors[bit]['missing']
            )

    # If there are unparsed tokens left, there were bad arguments supplied
    if bits:
        raise template.TemplateSyntaxError("Bad arguments supplied")

    return FlatContentNode(slug, **kwargs)

register.tag('flatcontent', do_flatcontent)
