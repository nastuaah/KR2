import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kr2.settings')
django.setup()

from myApp.models import FlowerShop, AboutSection


def load_flower_shop_data():
    print("Начало загрузки данных цветочного магазина...")

    shop_data = {
        "name": "Astro Flowers",
        "tagline": "цветочный салон",
        "description": "Самые свежие цветы со всего мира, для самых дорогих сердцу людей.",
        "delivery_info": "Круглосуточная доставка букетов по Нижнему Новгороду!",
        "image": "home.jpg"
    }

    about_sections = [
        {
            'title': 'О нас',
            'content': 'Свежие цветы со всего мира, собранные с любовью, чтобы радовать самых дорогих сердцу людей.'
        },
        {
            'title': 'О нас',
            'content': 'Независимо от повода — будь то праздник, признание в любви или просто желание подарить улыбку.'
        }
    ]

    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'kr2', 'myApp', 'static')

    try:
        shop = FlowerShop(
            name=shop_data['name'],
            tagline=shop_data['tagline'],
            description=shop_data['description'],
            delivery_info=shop_data['delivery_info']
        )

        image_path = os.path.join(static_dir, shop_data['image'])
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                shop.main_image.save(shop_data['image'], File(f))
            shop.save()
            print(f"Успешно создан магазин: {shop.name}")
        else:
            print(f"Ошибка: файл {shop_data['image']} не найден в {static_dir}")
            return

        for section in about_sections:
            AboutSection.objects.create(
                shop=shop,
                title=section['title'],
                content=section['content']
            )
            print(f"Добавлен раздел: {section['title']}")

    except Exception as e:
        print(f"Ошибка при создании магазина: {str(e)}")
        return

    print("Данные успешно загружены!")


if __name__ == '__main__':
    load_flower_shop_data()