import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kr2.settings')
django.setup()

from myApp.models import Student, Teacher, Classmate


def create_education_data():
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'kr2', 'myApp', 'static')

    student_data = {
        "name": "Хоменко Анастасия Максимовна",
        "email": "amkhomenko_1@edu.hse.ru",
        "phone": "+79087270757",
        "program": "Бизнес-информатика",
        "program_description": """
        «Бизнес-информатика» представляет собой междисциплинарное направление, интегрирующее такие дисциплины, как 
        информатика, математика, экономика, менеджмент. По определению IEEE Conference on Business Informatics 
        «Бизнес-информатика представляет собой научное направление, ориентированное на изучение информационных процессов  
        и связанных с ними явлений в социально-экономическом и бизнес контексте…»
        """
    }

    try:
        student = Student(**student_data)
        student_photo_path = os.path.join(static_dir, 'anastasia.jpg')
        if os.path.exists(student_photo_path):
            with open(student_photo_path, 'rb') as f:
                student.photo.save('anastasia.jpg', File(f))
        student.save()
        print(f"Успешно создан студент: {student.name}")
    except Exception as e:
        print(f"Ошибка при создании студента: {str(e)}")
        return

    teachers_data = [
        {
            "name": "Улитин Борис Игоревич",
            "photo": "ulitin.jpg",
            "email": "bulitin@hse.ru",
            "subjects": "Информационные системы, Базы данных"
        },
        {
            "name": "Емельянова Мария Максимовна",
            "photo": "emelyanova.jpg",
            "email": "example@hse.ru",
            "subjects": "Экономика, Менеджмент"
        }
    ]

    for data in teachers_data:
        try:
            teacher = Teacher(
                name=data['name'],
                email=data['email'],
                subjects=data['subjects']
            )
            image_path = os.path.join(static_dir, data['photo'])
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    teacher.photo.save(data['photo'], File(f))
            teacher.save()
            print(f"Успешно создан преподаватель: {teacher.name}")
        except Exception as e:
            print(f"Ошибка при создании преподавателя {data['name']}: {str(e)}")

    classmates_data = [
        {
            "name": "Лумбова Софья Игоревна",
            "photo": "sofia.jpg",
            "email": "silumbova@edu.hse.ru",
            "phone": "+79038482926"
        },
        {
            "name": "Щапова Майя Алексеевна",
            "photo": "maya.jpg",
            "email": "maschapova@edu.hse.ru",
            "phone": "+79200516002"
        }
    ]

    for data in classmates_data:
        try:
            classmate = Classmate(
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                student=student
            )
            image_path = os.path.join(static_dir, data['photo'])
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    classmate.photo.save(data['photo'], File(f))
            classmate.save()
            print(f"Успешно создан сокурсник: {classmate.name}")
        except Exception as e:
            print(f"Ошибка при создании сокурсника {data['name']}: {str(e)}")


if __name__ == '__main__':
    print("Начало заполнения базы данных...")
    create_education_data()
    print("Заполнение завершено!")