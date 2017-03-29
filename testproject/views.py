from django.views.generic import TemplateView as DjangoTemplateView


class TemplateView(DjangoTemplateView):
    context = None

    def get_context_data(self, *args, **kwargs):
        context = super(TemplateView, self).get_context_data(*args, **kwargs)
        context.update(self.context or {})
        return context
