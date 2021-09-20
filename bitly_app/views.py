from django.shortcuts import render
from django.views.generic.base import View, RedirectView

from bitly.settings import cache
from bitly_app.forms import LongURLForm
import hashlib


backend = '127.0.0.1:8000/'


class ConvertView(View):
    form_class = LongURLForm
    template_name = 'bitly_app/convert.html'
    context_object_name = 'main'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            url = form.cleaned_data['long_url']
            hash_url = hashlib.md5(url.encode()).hexdigest()[:10]
            if not cache.hexists(hash_url, url):
                shorten_url = backend + hash_url
                cache.hset(hash_url, url, shorten_url)

            result = cache.hget(hash_url, url)
            context = {
                'form': self.form_class(),
                'url': url,
                'shorten_url': result.decode()
            }

            return render(request, 'bitly_app/success.html', context)
        else:
            form = self.form_class()
        return render(request, self.template_name, {'form': form})


class RedirectTo(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        hash = kwargs.get('hash_url')
        url = cache.hkeys(hash)[0]
        return url.decode()




