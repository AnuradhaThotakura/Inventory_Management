from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Item
from .serializers import ItemSerializer
from django.core.cache import cache  # Import the cache
import logging

logger = logging.getLogger(__name__)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def retrieve(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')  # Get the item ID from the URL
        cache_key = f'item_{item_id}'  # Create a cache key based on item ID

        # Try to get the item from cache
        item_data = cache.get(cache_key)
        print("item_data",item_data)
        if item_data is not None:
            logger.info(f"Item {item_id} fetched from cache.")
            return Response(item_data)

        # If not in cache, retrieve from the database
        try:
            item = self.get_object()  # Retrieve the item based on the provided ID
            serializer = self.get_serializer(item)
            # Store the item in cache for future requests
            cache.set(cache_key, serializer.data, timeout=60 * 5)  # Cache for 5 minutes
            logger.info(f"Item {item_id} fetched from database and cached.")
            return Response(serializer.data)  # Return serialized item data
        except Item.DoesNotExist:
            logger.error(f"Item {item_id} not found in database.")
            raise NotFound(detail="Item not found.", code=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')  # Get the item ID
        logger.info(f"Attempting to update item {item_id}.")
        
        try:
            item = self.get_object()  # Get the item instance to update
        except Item.DoesNotExist:
            logger.error(f"Item {item_id} not found for update.")
            return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

        # If item exists, proceed to update
        serializer = self.get_serializer(item, data=request.data, partial=True)  # Update with provided data
        serializer.is_valid(raise_exception=True)  # Validate the data
        serializer.save()  # Save the updated item

        # Invalidate the cache after updating
        cache_key = f'item_{item.id}'
        cache.delete(cache_key)  # Remove the old cache entry
        logger.info(f"Item {item_id} updated successfully.")
        
        return Response(serializer.data)  # Return the updated item data

    def destroy(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')  # Get the item ID
        logger.info(f"Attempting to delete item {item_id}.")

        try:
            item = self.get_object()  # Retrieve the item to delete
            item.delete()  # Delete the item

            # Invalidate the cache after deletion
            cache_key = f'item_{item.id}'
            cache.delete(cache_key)  # Remove the cache entry
            logger.info(f"Item {item_id} deleted successfully.")
            
            return Response({"detail": "Item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            logger.error(f"Item {item_id} not found for deletion.")
            raise NotFound(detail="Item not found.", code=status.HTTP_404_NOT_FOUND)
