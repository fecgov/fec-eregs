from bs4 import BeautifulSoup
from django.test import TestCase
import os.path

class PartialDefinitionTests(TestCase):
    def fixture_path(self, fixture_name='default'):
        test_dir = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(test_dir, 'fixtures', fixture_name) + os.sep

    def test_definition_with_ambiguous_paragraphs(self):
        with self.settings(API_BASE=self.fixture_path('definition_with_ambiguous_paragraph')):
            response = self.client.get('/partial/definition/100-5/2015-annual-100')

            self.assertTemplateUsed('parital-definition.html')
            self.assertContains(response, 'The first piece of this definition is:')
            self.assertContains(response, 'See the full definition at:')
            self.assertContains(response, 'Political committee means any group meeting one of the following conditions:')
