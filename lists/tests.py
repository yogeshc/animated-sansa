from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item


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

        self.assertEqual(Item.objects.all().count(), 1)
        new_item = Item.objects.all()[0]
        self.assertEqual(new_item.text, 'A new list item')

        # We no longer expect a response with a .content rendered by
        # a template, so we lose the assertions that look at that.
        # Instead, the response will represent an HTTP redirect, which
        # should have status code 302, and points the browser towards
        # a new location.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_home_page_displays_all_test_items(self):
        Item.objects.create(text='listItem 1')
        Item.objects.create(text='listItem 2')

        request = HttpRequest()
        response = home_page(request)

        self.assertIn('listItem 1', response.content)
        self.assertIn('listItem 2', response.content)


class ItemModelTest(TestCase):
    """
    You can see that creating a new record in the database is a relatively
    simple matter of creating an object, assigning some attributes, and
    calling a .save() function. Django also gives us an API for querying the
    database via a class method, .objects, and we use the simplest possible
    query, .all(), which retrieves all the records for that table. The
    results are returned as a list-like object called a QuerySet, which
    we can call further functions on, like .count(), and also extract
    individual objects. We then check the objects as saved to the database,
    to check whether the right information was saved
    """

    def test_saving_and_retriving_items(self):
        first_item = Item()
        first_item.text = 'The first list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second list item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first list item')
        self.assertEqual(second_saved_item.text, 'The second list item')

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)
