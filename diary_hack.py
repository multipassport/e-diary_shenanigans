import random

from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation

PRAISES = (
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
    )


def get_child_model(kid_name):
    try:
        child = Schoolkid.objects.get(full_name__contains=kid_name)
    except Schoolkid.DoesNotExist:
        print('Такой ученик не существует')
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено больше одного совпадения. Уточните имя')
    else:
        return child


def fix_marks(kid_name):
    child = get_child_model(kid_name)
    marks = Mark.objects.filter(schoolkid=child, points__in=[2, 3])
    for mark in marks:
        mark.points = 5
        mark.save()


def remove_chastisements(kid_name):
    child = get_child_model(kid_name)
    chasticements = Chastisement.objects.filter(schoolkid=child)
    for chasticement in chasticements:
        chasticements.delete()


def create_commendation(kid_name, subject_name):
    text = random.choice(PRAISES)
    child = get_child_model(kid_name)
    if child:
        school_grade = child.year_of_study
        group_letter = child.group_letter
        try:
            lesson = Lesson.objects.filter(
                year_of_study=school_grade,
                group_letter=group_letter,
                subject__title=subject_name
                ).last()
            lesson_date = lesson.date
            teacher = lesson.teacher
            subject = lesson.subject
        except AttributeError:
            print('Неверное имя предмета')
        else:
            Commendation.objects.create(
                text=text,
                created=lesson_date,
                schoolkid=child,
                subject=subject,
                teacher=teacher,
                )
