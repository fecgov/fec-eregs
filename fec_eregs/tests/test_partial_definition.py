from django.test import Client, TestCase
from regcore.models import Regulation
from bs4 import BeautifulSoup


class PartialDefinitionTests(TestCase):
    def test_definition_with_ambiguous_paragraphs(self):
        regulation = Regulation()
        regulation.label_string = '100-5'
        regulation.text = 'In this section, document means the following:'
        regulation.title = 'A Regulation Title'
        #regulation.children.append(Regulation())
        regulation.save()

        client = Client()
        response = client.get('/partial/definition/100-5/2015-annual-100')

        partial = BeautifulSoup(response.content)
        self.assertTrue(partial.select('.definition-text p').text.contains('The first piece of this definition is:'))
        self.assertTrue(partial.select('.definition-text p').text.contains('See the full definition at:'))
        self.assertEqual(partial.select('.definition-text blockquote').text, regulation.text)
