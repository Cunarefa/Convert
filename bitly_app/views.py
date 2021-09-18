from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View

from bitly.settings import cache
from bitly_app.forms import LongURLForm
import hashlib
import pyshorteners


shortener = pyshorteners.Shortener()


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
            hash_url = hashlib.md5(url.encode()).hexdigest()
            if not cache.hexists(hash_url, url):
                short_url = shortener.tinyurl.short(url)
                cache.hset(hash_url, url, short_url)

            result = cache.hget(hash_url, url)
            context = {
                'form': self.form_class(),
                'url': url,
                'shorten_link': result.decode()
            }

            return render(request, 'bitly_app/success.html', context)
        else:
            form = self.form_class()
        return render(request, self.template_name, {'form': form})





