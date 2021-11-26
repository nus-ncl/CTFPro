from django.test import TestCase

# Create your tests here.


class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get('/vms/')
        self.assertEqual(response.status_code, 200)
        
