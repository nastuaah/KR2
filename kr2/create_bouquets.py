import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kr2.settings')
django.setup()

from myApp.models import Bouquet


def create_bouquets():
    bouquets_data = [
        {"name": "Ранункулюсы", "price": 4950, "image": "catalogue1.jpg"},
        {"name": "Букет 'Tiara'", "price": 5000, "image": "catalogue2.jpg"},
        {"name": "Пионовидные розы", "price": 6000, "image": "catalogue3.jpg"},
        {"name": "Пионы", "price": 7000, "image": "catalogue4.jpg"},
        {"name": "Цветочная сумочка", "price": 7000, "image": "catalogue5.jpg"},
        {"name": "Wow Букет", "price": 20000, "image": "catalogue6.jpg"},
        {"name": "Тюльпаны", "price": 4000, "image": "catalogue7.jpg"},
        {"name": "Букет 'Strawberry Coctail'", "price": 6200, "image": "catalogue8.jpg"},
        {"name": "С пионами", "price": 5850, "image": "catalogue9.jpg"},
    ]

    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'kr2', 'myApp', 'static')

    for data in bouquets_data:
        try:
            bouquet = Bouquet(
                name=data['name'],
                price=data['price']
            )

            image_path = os.path.join(static_dir, data['image'])

            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    bouquet.image.save(data['image'], File(f))
                bouquet.save()
                print(f"Успешно создан букет: {bouquet.name}")
            else:
                print(f"Ошибка: файл {data['image']} не найден в {static_dir}")
        except Exception as e:
            print(f"Ошибка при создании букета {data['name']}: {str(e)}")


if __name__ == '__main__':
    print("Начало заполнения базы данных...")
    create_bouquets()
    print("Заполнение завершено!")