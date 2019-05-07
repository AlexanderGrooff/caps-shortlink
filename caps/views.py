from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from urllib3.util import parse_url

from caps.models import LinkModel
from .forms import ShortenerForm


@ensure_csrf_cookie
def get_long_url(request):
    if request.method == 'POST':
        form = ShortenerForm(request.POST)
        if form.is_valid():
            link = LinkModel(**form.cleaned_data)
            link.save()
            print("Created new link for checksum {} to {}".format(link.checksum, link.long_url))
            return redirect("/?SUM={}".format(link.checksum))
    else:
        form = ShortenerForm()
        template_vars = {'form': form}
        if request.GET.get('SUM'):
            try:
                link = LinkModel.objects.get(checksum=request.GET.get('SUM'))
            except ObjectDoesNotExist:
                pass
            else:
                template_vars['link'] = link
        return render(request, 'main.html', template_vars)


def redirect_checksum(request, checksum):
    print("Redirecting from checksum {}".format(checksum))
    try:
        link = LinkModel.objects.get(checksum=checksum)
    except ObjectDoesNotExist:
        raise Http404
    else:
        url = link.long_url
        urlparse_obj = parse_url(url)
        if not urlparse_obj.scheme:
            url = "http://{}".format(url)
        print("Redirecting to {}".format(url))
        return redirect(url)
