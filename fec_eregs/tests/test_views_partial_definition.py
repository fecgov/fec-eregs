from unittest import TestCase
from django.template import loader, Context


class PartialDefinitionTests(TestCase):
    urls = 'regulation.urls'

    def test_partial_definition_with_children(self):
        t = loader.get_template('regulations/partial-definition.html')

        node = {
            'section_id': '100-5',
            'label_id': '100-5',
            'children': [{'label_id': '100-5-a'}],
            'marked_up': 'Political committee means any group meeting one of the following conditions:',
        }

        context_dict = {'node': node, 'version': '2015-annual'}
        response = t.render(Context(context_dict))

        first_paragraph = 'The first piece of this definition is:'
        see_full_definition = 'See the full definition at:'
        self.assertTrue(first_paragraph in response)
        self.assertTrue(see_full_definition in response)
        self.assertTrue(node['marked_up'] in response)

    def test_partial_definition_no_children(self):
        t = loader.get_template('regulations/partial-definition.html')

        node = {
            'section_id': '102-4',
            'label_id': '202-2-a',
            'marked_up': 'This term is defined carefully'
        }

        context_dict = {'node': node, 'version': '2012-1223'}
        response = t.render(Context(context_dict))

        self.assertTrue(node['marked_up'] in response)
        first_paragraph = 'The first piece of this definition is:'
        see_full_definition = 'See the full definition at:'
        self.assertFalse(first_paragraph in response)
        self.assertFalse(see_full_definition in response)

    def test_partial_definition_with_children_no_text(self):
        t = loader.get_template('regulations/partial-definition.html')

        node = {
            'section_id': '100-5',
            'label_id': '100-5',
            'children': [{'label_id': '100-5-a'}],
        }

        context_dict = {'node': node, 'version': '2015-annual'}
        response = t.render(Context(context_dict))

        first_paragraph = 'The first piece of this definition is:'
        best_viewed = 'This definition is best viewed in its original location.'
        see_full_definition = 'See the full definition at:'
        self.assertFalse(first_paragraph in response)
        self.assertTrue(see_full_definition in response)
        self.assertTrue(best_viewed in response)

