import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kr2.settings')
django.setup()

from myApp.models import ShopInfo


def create_shop_info():
    shop_data = {
        "phone": "+7 (910) 790-45-35",
        "address": "г. Н.Новгород, ул.Ильинская 31",
        "working_hours": "Круглосуточно",
        "image": "info.jpg"
    }

    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'kr2', 'myApp', 'static')

    try:
        ShopInfo.objects.all().delete()

        shop = ShopInfo(
            phone=shop_data['phone'],
            address=shop_data['address'],
            working_hours=shop_data['working_hours']
        )

        image_path = os.path.join(static_dir, shop_data['image'])

        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                shop.image.save(shop_data['image'], File(f))
            shop.save()
            print(f"Успешно создана запись ShopInfo с изображением {shop_data['image']}")
        else:
            shop.save()
            print(f"Ошибка: файл {shop_data['image']} не найден в {static_dir}. Запись создана без изображения.")

    except Exception as e:
        print(f"Ошибка при создании ShopInfo: {str(e)}")


if __name__ == '__main__':
    print("Начало загрузки данных магазина...")
    create_shop_info()
    print("Загрузка завершена!")