from django.core.management.base import BaseCommand
from restaurant.models import Item

class Command(BaseCommand):
    help = 'Populates the database with predefined items'

    def handle(self, *args, **kwargs):
        Item.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all existing items.'))

        # Define item data with Chinese cuisine and more
        item_data = [
            {'name': 'Kung Pao Chicken', 'description': 'Spicy stir-fried chicken with peanuts, vegetables, and chili peppers.', 'price': 12.99, 'category': 'entree'},
            {'name': 'Mapo Tofu', 'description': 'Spicy and hot tofu dish with minced meat (usually pork or beef), fermented beans, and chili oil.', 'price': 10.99, 'category': 'entree'},
            {'name': 'Peking Duck', 'description': 'A famous duck dish from Beijing that has been prepared since the imperial era, featuring crispy skin and tender meat.', 'price': 25.99, 'category': 'entree'},
            {'name': 'Dumplings', 'description': 'Dough pieces filled with meat and vegetables, typically steamed or fried.', 'price': 8.99, 'category': 'appetizer'},
            {'name': 'Hot and Sour Soup', 'description': 'A rich broth containing ingredients such as mushrooms, bamboo shoots, tofu, and pork.', 'price': 7.99, 'category': 'appetizer'},
            {'name': 'Sweet and Sour Pork', 'description': 'Deep fried pork chunks with a sweet and sour sauce, served with green and red peppers.', 'price': 11.99, 'category': 'entree'},
            {'name': 'Green Tea', 'description': 'Freshly brewed green tea, known for its health benefits and soothing properties.', 'price': 2.99, 'category': 'beverage'},
            {'name': 'Bubble Tea', 'description': 'Sweet, milky tea with tapioca pearls, a popular Taiwanese drink.', 'price': 4.99, 'category': 'beverage'},
            {'name': 'Mango Pudding', 'description': 'A refreshing dessert made from mangoes, cream, and sugar, set into a soft pudding.', 'price': 5.99, 'category': 'dessert'},
            {'name': 'Egg Tart', 'description': 'A sweet pastry crust filled with a smooth, creamy egg custard, baked to perfection.', 'price': 3.99, 'category': 'dessert'}
        ]

        # Create each item if it doesn't already exist
        for item_info in item_data:
            item_name = item_info['name']
            description = item_info['description']
            price = item_info['price']
            category = item_info['category']

            # Check if the item already exists
            if not Item.objects.filter(name=item_name).exists():
                Item.objects.create(name=item_name, description=description, price=price, category=category)
                self.stdout.write(self.style.SUCCESS(f'Successfully created {item_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'{item_name} already exists. No changes made.'))

