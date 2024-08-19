from django.db import models, connection

# нет локаций
# есть сценарии
#   которые где-то используются? или просто еесть?
# TODO если он должен где-то использоваться, значит надо делать join с квестом
SQL_TASK_1 = """
SELECT COUNT(*) FROM polls_partner
WHERE NOT EXISTS(SELECT * FROM polls_location 
             WHERE polls_location.partner_id == polls_partner.id)
      AND EXISTS(SELECT * FROM polls_legend
                 WHERE polls_legend.partner_id == polls_partner.id)
;
"""

# девушек стравниваем между другими девукшами или воббще со всеми?
# должны получить среднее время прохождение под руководством девушек
#     выбрать наименьшее в случае конфликта лексографически
#  сортировка не нужна, он вроде и так правильно выводил
SQL_TASK_2 = """
SELECT name, min(duration) FROM (
    SELECT polls_partner.name as name, AVG(polls_game.time_duration) AS duration FROM polls_partner
    JOIN polls_location ON polls_partner.id == polls_location.partner_id
    JOIN polls_quest ON polls_location.id == polls_quest.location_id
    JOIN polls_game ON polls_quest.id == polls_game.quest_id
    JOIN polls_employee ON polls_employee.id == polls_game.employee_id
    WHERE polls_employee.gender == True 
          and polls_game.is_full_complite == True
    GROUP BY polls_partner.name
    ORDER BY duration, name ASC
);
"""

SQL_TASK_3 = """
"""


def my_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()


class Partner(models.Model):
    name = models.CharField("Название партнера", max_length=50, unique=True)

    @classmethod
    def task_1(cls):
        with connection.cursor() as cursor:
            cursor.execute(SQL_TASK_1)
            return cursor.fetchone()

    @classmethod
    def task2(self):
        return my_query(SQL_TASK_2)


class Location(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    city_name = models.CharField('Название города', max_length=50)
    metro = models.CharField("Ближайшее метро", max_length=50)


class Legend(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    legend = models.CharField("Название сюжета", max_length=100, unique=True)
    complexity = models.IntegerField("Сложность квеста", default=1)


class Quest(models.Model):
    legend = models.ForeignKey(Legend, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField("Название квеста", max_length=100)


class Employee(models.Model):
    first_name = models.CharField("Имя сотрудника", max_length=50)
    last_name = models.CharField("Фамилия сотрудника", max_length=50)
    gender = models.BooleanField("Под сотрудника")


class Game(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_start = models.DateTimeField("Дата мероприятия")
    price = models.IntegerField("Cтоимость игры")
    game_has_passed = models.BooleanField("Игра состоялась")
    is_full_complite = models.BooleanField("Полностью пройден", default=False)
    time_duration = models.IntegerField("Вермя прохождения")


class Calendar(models.Model):
    day = models.IntegerField("День")
    year = models.IntegerField("Год")
    month = models.CharField("Название месяца", max_length=20)
    day_of_month_no = models.IntegerField("Номер дня внутри месяца")
    day_of_week_no = models.IntegerField("Название для недели")
    is_holiday = models.BooleanField("Выходной или празничный", default=False)
