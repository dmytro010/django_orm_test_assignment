from django.test import RequestFactory
from django.test.utils import setup_test_environment, teardown_test_environment
from django.http import HttpResponse
from django.template import Context, Template
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import path, reverse
import requests
import unittest

"""
TASK:
The code below defines the template and view that generates a list of facts about cats.
The particular facts are fetched from the third-party API. 
Implement the unit test to test the view using a mocking technique to avoid using 
the third-party API during tests.
"""

TEMPLATE = '''
<h3>Cat facts</h3>

<ul>
    {% for fact in facts %}
    <li>{{ fact }}</li>
    {% endfor %}
</ul>
'''

def cat_facts(request):
    response = requests.get('https://cat-fact.herokuapp.com/facts')
    facts = [x['text'] for x in response.json()]
    
    template = Template(TEMPLATE)
    context = Context({
        'facts': facts,
    })
    return HttpResponse(template.render(context))
    
# Implement the unit tests here

urlpatterns = [
    path('/facts/', cat_facts, name='facts'),
]

@override_settings(ROOT_URLCONF=__name__)
class CatFactsTest(TestCase):
    def setUp(self):
        setup_test_environment()

    def tearDown(self):
        teardown_test_environment()

       
    def test_view(self):
        facts_url = reverse('facts')
        
        # Replace this with the test implementation

        self.assertEqual(True, True)

        
unittest.main(argv=[''], verbosity=2, exit=False)

        
# from IPython.core.display import HTML
# factory = RequestFactory()
# request = factory.get('/facts/')
# HTML(
#     cat_facts(request).content.decode()  # Render the current order
# )