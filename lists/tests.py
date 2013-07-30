"""
Django's main job is to decide what to do when a user asks for a particular URL on our site. 
Django's workflow goes something like this: 
1. An HTTP request comes in for a particular URL.
2. Django uses some rules to decide which view function 
should deal with that request (this is referred to as resolving the URL) 
3. The view function processes the request and returns an HTTP response.

So we want to test two things: 
1. Can we resolve the URL for the root of the site ("/") to a particular view function? 
2. Can we make this view function return some HTML (which will get the functional test to pass)?

"""



from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func,home_page)
