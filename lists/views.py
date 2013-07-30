# Create your views here.
from django.http import HttpRequest, HttpResponse

def home_page(requests):
  response = HttpResponse('<html> <title>To-Do Lists</title> </html>')
  return response
