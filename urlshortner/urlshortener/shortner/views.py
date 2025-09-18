from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import URLMapping
from .utils import generate_unique_short_key
import json
from django.shortcuts import render
from django.conf import settings

@csrf_exempt
def shorten_url(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            original_url = data.get('url')
            if not original_url:
                return JsonResponse({'error': 'URL is required'}, status=400)

            short_key = generate_unique_short_key()
            url_mapping = URLMapping(short_key=short_key, original_url=original_url)
            url_mapping.save()
            host = request.get_host()
            short_url = f"http://{host}/{short_key}"

            return JsonResponse({'short_url': short_url}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"error": "POST method required"}, status=405)

def redirect_to_original(request, short_key):
    mapping = get_object_or_404(URLMapping, short_key=short_key)
    return HttpResponseRedirect(mapping.original_url)


def index(request):
    context = {}
    if request.method == 'POST':
        original_url = request.POST.get('url', '').strip()
        if not original_url:
            context['error'] = "Please enter a valid URL."
        else:
            if not (original_url.startswith('http://') or original_url.startswith('https://')):
                context['error'] = "URL must start with http:// or https://"
            else:
                try:
                    from .utils import generate_unique_short_key
                    from .models import URLMapping

                    short_key = generate_unique_short_key()
                    url_mapping = URLMapping(short_key=short_key, original_url=original_url)
                    url_mapping.save()

                    host = request.get_host()
                    short_url = f"http://{host}/shorten/{short_key}"
                    context['short_url'] = short_url
                except Exception as e:
                    context['error'] = f"Error: {str(e)}"

    return render(request, '/shortner/index.html', context)
