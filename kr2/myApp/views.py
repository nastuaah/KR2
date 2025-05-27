# Create your views here.
import re

from django.shortcuts import render, redirect
from .models import Bouquet, Order, Student, Classmate,Teacher, FlowerShop, ShopInfo
from django.db.models import Sum, Avg, Count, Max
from django.contrib import messages

def home(request):
    shop = FlowerShop.objects.first()
    return render(request, 'home.html', {'shop': shop})

def catalogue(request):
    bouquets = Bouquet.objects.all()

    search_query = request.GET.get('search', '')
    if search_query:
        bouquets = bouquets.filter(name__icontains=search_query)

    sort_by = request.GET.get('sort', '')
    print(f"Sort by: {sort_by}")

    if sort_by == 'name_asc':
        bouquets = bouquets.order_by('name')
    elif sort_by == 'name_desc':
        bouquets = bouquets.order_by('-name')
    elif sort_by == 'price_asc':
        bouquets = bouquets.order_by('price')
    elif sort_by == 'price_desc':
        bouquets = bouquets.order_by('-price')

    context = {
        'bouquets': bouquets,
        'search_query': search_query,
        'current_sort': sort_by,
    }
    return render(request, "catalogue.html", context)


def contacts(request):
    shop_info = ShopInfo.objects.first()
    bouquets = Bouquet.objects.all()
    search_query = request.GET.get('search', '').strip()
    client_orders = None
    expensive_order = None
    cheap_order = None

    if search_query:
        client_orders = Order.objects.filter(
            last_name__icontains=search_query
        ).order_by('-created_at')

        if client_orders.exists():
            expensive_order = client_orders.order_by('-price').first()
            cheap_order = client_orders.order_by('price').first()

            show_option = request.GET.get('show')
            if show_option == 'expensive':
                client_orders = [expensive_order]
            elif show_option == 'cheap':
                client_orders = [cheap_order]

    if request.method == 'POST':
        try:
            last_name = request.POST.get('last_name', '').strip()
            first_name = request.POST.get('first_name', '').strip()
            phone = request.POST.get('phone', '').strip()
            bouquet_id = request.POST.get('bouquet')
            comment = request.POST.get('comment', '').strip()

            errors = []

            if not last_name:
                errors.append('Фамилия обязательна для заполнения')
            elif not re.fullmatch(r'[А-ЯЁ][А-Яа-яЁё\s\-]*', last_name):
                errors.append(
                    'Фамилия должна начинаться с заглавной буквы и содержать только буквы, пробелы и дефисы')

            if not first_name:
                errors.append('Имя обязательно для заполнения')
            elif not re.fullmatch(r'[А-ЯЁ][А-Яа-яЁё\s\-]*', first_name):
                errors.append('Имя должно начинаться с заглавной буквы и содержать только буквы, пробелы и дефисы')

            if not phone:
                errors.append('Телефон обязателен для заполнения')
            else:
                phone_digits = re.sub(r'\D', '', phone)
                if phone_digits.startswith('8'):
                    phone_digits = '7' + phone_digits[1:]
                if not phone_digits.startswith('7'):
                    errors.append('Телефон должен начинаться с +7')
                elif len(phone_digits) != 11:
                    errors.append('Номер телефона должен содержать 11 цифр')
                else:
                    phone = f"+7({phone_digits[1:4]}){phone_digits[4:7]}-{phone_digits[7:9]}-{phone_digits[9:11]}"

            if not bouquet_id:
                errors.append('Необходимо выбрать букет')

            if errors:
                for error in errors:
                    messages.error(request, error)
            else:
                bouquet = Bouquet.objects.get(id=bouquet_id)
                Order.objects.create(
                    last_name=last_name.capitalize(),
                    first_name=first_name.capitalize(),
                    phone=phone,
                    bouquet=bouquet,
                    comment=comment,
                    price=bouquet.price
                )
                messages.success(request, 'Ваш заказ успешно оформлен!')
                return redirect(request.path)

        except Bouquet.DoesNotExist:
            messages.error(request, 'Выбранный букет не найден')
        except Exception as e:
            messages.error(request, f'Произошла ошибка: {str(e)}')
        return redirect(request.path)

    order_stats = Order.objects.aggregate(
        total_orders=Count('id'),
        total_revenue=Sum('price'),
        avg_order=Avg('price')
    )

    contact_requests = Order.objects.all().order_by('-created_at')[:10]

    context = {
        'shop_info': shop_info,
        'bouquets': bouquets,
        'contact_requests': contact_requests,
        'order_stats': order_stats,
        'search_query': search_query,
        'client_orders': client_orders,
        'expensive_order': expensive_order,
        'cheap_order': cheap_order
    }

    return render(request, 'contacts.html', context)


def about(request):
    student = Student.objects.first()
    teachers = Teacher.objects.all()
    classmates = Classmate.objects.filter(student=student)

    name_filter = request.GET.get('name')
    sort_by = request.GET.get('sort')

    if name_filter:
        teachers = teachers.filter(name__icontains=name_filter)
        classmates = classmates.filter(name__icontains=name_filter)

    if sort_by:
        teachers = teachers.order_by(sort_by)
        classmates = classmates.order_by(sort_by)

    context = {
        "student": student,
        "teachers": teachers,
        "classmates": classmates,
        "filters": {
            "name": name_filter or '',
            "sort": sort_by or ''
        }
    }

    return render(request, "about.html", context)