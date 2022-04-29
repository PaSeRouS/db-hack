from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
import random

from datacenter.models import Chastisement, Commendation
from datacenter.models import Lesson, Mark
from datacenter.models import Schoolkid, Subject, Teacher

def get_student(name):
    try:
        return Schoolkid.objects.get(full_name__contains = name)
    except MultipleObjectsReturned:
        print("С таким именем в школе есть несколько человек. Уточните, пожалуйста, имя!")
    except ObjectDoesNotExist:
        print("С таким именем в школе никого нет. Введите другое имя")


def fix_marks(name):
    schoolkid = get_student(name)
    marks = Mark.objects.filter(schoolkid = schoolkid, points__in = [2, 3])

    for mark in marks:
        mark.points = 5
        mark.save()


def remove_chastisements(name):
    schoolkid = get_student(name)
    Chastisement.objects.filter(schoolkid = schoolkid).delete()


def create_commendation(name, subject):
    student = get_student(name)

    try:
        subject = Subject.objects.get(title = subject, year_of_study = student.year_of_study)
        lesson = random.choice(Lesson.objects.filter(year_of_study = student.year_of_study, group_letter = student.group_letter, subject = subject).order_by('-date'))
        
        commendations = [
            'Молодец!',
            'Отлично!',
            'Хорошо!',
            'Гораздо лучше, чем я ожидал!',
            'Ты меня приятно удивил!',
            'Великолепно!',
            'Прекрасно!',
            'Ты меня очень обрадовал!',
            'Именно этого я давно ждал от тебя!',
            'Сказано здорово – просто и ясно!',
            'Ты, как всегда, точен!',
            'Очень хороший ответ!',
            'Талантливо!',
            'Ты сегодня прыгнул выше головы!',
            'Я поражен!',
            'Уже существенно лучше!',
            'Потрясающе!',
            'Замечательно!',
            'Прекрасное начало!',
            'Так держать!',
            'Ты на верном пути!',
            'Здорово!',
            'Это как раз то, что нужно!',
            'Я тобой горжусь!',
            'С каждым разом у тебя получается всё лучше!',
            'Мы с тобой не зря поработали!',
            'Я вижу, как ты стараешься!',
            'Ты растешь над собой!',
            'Ты многое сделал, я это вижу!',
            'Теперь у тебя точно все получится!',
        ]
        
        Commendation.objects.create(text = random.choice(commendations), created = lesson.date, schoolkid = student, subject = subject, teacher = lesson.teacher)
    except ObjectDoesNotExist:
        print('Такого предмета у этого ученика нет. Введите другой предмет!')