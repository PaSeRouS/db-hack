import random
from textwrap import dedent

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from datacenter.models import Chastisement, Commendation
from datacenter.models import Lesson, Mark
from datacenter.models import Schoolkid, Subject, Teacher


def get_student(name):
    try:
        return Schoolkid.objects.get(full_name__contains=name)
    except MultipleObjectsReturned:
        print(dedent("""\
            С таким именем в школе есть несколько человек.
            Уточните, пожалуйста, имя!"""))
    except ObjectDoesNotExist:
        print("С таким именем в школе никого нет. Введите другое имя")


def fix_marks(name):
    schoolkid = get_student(name)

    if not schoolkid:
        return

    marks = Mark.objects.filter(
        schoolkid=schoolkid,
        points__in=[2, 3]
    )

    for mark in marks:
        mark.points = 5
        mark.save()


def remove_chastisements(name):
    schoolkid = get_student(name)

    if schoolkid:
        Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(name, subject):
    student = get_student(name)

    if not student:
        return

    subject_exist = True

    try:
        subject = Subject.objects.get(
            title=subject,
            year_of_study=student.year_of_study
        )
    except ObjectDoesNotExist:
        subject_exist = False
        print(dedent('''\
            Такого предмета у этого ученика нет. Введите другой предмет!'''))

    if not subject_exist:
        return

    subject_lessons = Lesson.objects.filter(
            year_of_study=student.year_of_study,
            group_letter=student.group_letter,
            subject=subject
        ).order_by('-date')

    random_lesson = random.choice(subject_lessons)

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

    Commendation.objects.create(
        text=random.choice(commendations),
        created=random_lesson.date,
        schoolkid=student,
        subject=subject,
        teacher=random_lesson.teacher
    )
