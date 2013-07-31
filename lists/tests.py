from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):

        """
        Django's main job is to decide what to do when a user asks for a
        particular URL on our site.
        Django's workflow goes something like this:
        1. An HTTP request comes in for a particular URL.
        2. Django uses some rules to decide which view function should deal
        with that request (this is referred to as resolving the URL)
        3. The view function processes the request and returns an HTTP
        response.
        So we want to test two things:
        1. Can we resolve the URL for the root of the site
        ("/") to a particular view function?
        2. Can we make this view function return some HTML
        (which will get the functional test to pass)?
        """
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """
        We create an HttpRequest object, which is what Django will see when a
        user's browser asks for a page.
        We pass it to our home_page view, which should give us a response.
        (response is an object is of a class called HttpResponse.)
        We will assert that the content of the response
        (which is the HTML that we will send to the user)
        has certain properties.
            1. We want it to start with an < html > tag and end with </html>
            2. Also we want a <title> tag with the word To-Do in it because
                 we we have specified in our functional test.
        """
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith('<html>'))
        self.assertIn('<title>To-Do Lists</title>', response.content)
        self.assertTrue(response.content.strip().endswith('</html>'))

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content, expected_html)

    def test_home_page_can_save_POST_request(self):
        """
        Lets adapt the view to be able to deal with a POST request.
        Add our POST request, then check that the returned HTML
        will have the new item text in it:
        """
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        response = home_page(request)
        self.assertIn('A new list item', response.content)
        expected_html = render_to_string(
            'home.html', {'new_item_text': 'A new list item'}
        )
        self.assertEqual(response.content, expected_html)
