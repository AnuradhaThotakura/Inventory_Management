from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from .models import Item

class ItemAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.item_data = {
            "name": "Unique Test Item",
            "description": "Description of the test item."
        }
        cls.item = Item.objects.create(**cls.item_data)

    def test_create_item(self):
        new_item_data = {
            "name": "Another Unique Test Item",
            "description": "Another description."
        }
        response = self.client.post(reverse('items-list'), data=new_item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_duplicate_item(self):
        response = self.client.post(reverse('items-list'), data=self.item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_read_item(self):
        response = self.client.get(reverse('items-detail', args=[self.item.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset(self.item_data, response.data)

    def test_update_item(self):
        updated_data = {
            "name": "Updated Item",
            "description": "Updated description."
        }
        response = self.client.patch(reverse('items-detail', args=[self.item.id]), data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, updated_data['name'])

    def test_delete_item(self):
        response = self.client.get(reverse('items-detail', args=[self.item.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(reverse('items-detail', args=[self.item.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(reverse('items-detail', args=[self.item.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
