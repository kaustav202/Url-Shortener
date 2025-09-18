import random
import string
from .models import URLMapping

def generate_unique_short_key(length=10):
    characters = string.ascii_letters + string.digits
    while True:
        short_key = ''.join(random.choices(characters, k=length))
        if not URLMapping.objects.filter(short_key=short_key).exists():
            return short_key
