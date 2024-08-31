import datetime

from django.test import TestCase

from polls.models import Partner, Legend, Location, Quest, Employee, Game


class TestTaskOne(TestCase):
    def setUp(self):
        partner = Partner.objects.create(name="partner_name_1")
        # Location.objects.create(partner=partner, city_name="city_1", metro="metro_1")
        Legend.objects.create(partner=partner, legend="legend_name_1")

    def test_success(self):
        count_partners = Partner.task_1()[0]
        self.assertEqual(count_partners, 1)


class TestTaskTwo(TestCase):
    def setUp(self):
        partner = Partner.objects.create(name="partner_for_legend")
        legend = Legend.objects.create(partner=partner, legend="legend_name_1")

        partner_1 = Partner.objects.create(name="partner_name_1")
        partner_1_location = Location.objects.create(partner=partner_1, city_name="city_1", metro="metro_1")
        partner_1_quest = Quest.objects.create(legend=legend, location=partner_1_location, name="quest_1")
        employee1 = Employee.objects.create(first_name="name1", last_name="some_name", gender=False)
        Game.objects.create(quest=partner_1_quest, employee=employee1, date_start=datetime.datetime.now(),
             price=1, game_has_passed=True, is_full_complite=True, time_duration=20)

        partner_2 = Partner.objects.create(name="b")
        partner_2_location = Location.objects.create(partner=partner_2, city_name="city_1", metro="metro_1")
        partner_2_quest = Quest.objects.create(legend=legend, location=partner_2_location, name="quest_2")
        employee2 = Employee.objects.create(first_name="name2", last_name="some_name", gender=True)
        Game.objects.create(quest=partner_2_quest, employee=employee2, date_start=datetime.datetime.now(),
             price=1, game_has_passed=True, is_full_complite=True, time_duration=40)

        partner_3 = Partner.objects.create(name="a")
        partner_3_location = Location.objects.create(partner=partner_3, city_name="city_1", metro="metro_1")
        partner_3_quest = Quest.objects.create(legend=legend, location=partner_3_location, name="quest_3")
        employee3 = Employee.objects.create(first_name="name3", last_name="some_name", gender=True)
        Game.objects.create(quest=partner_3_quest, employee=employee3, date_start=datetime.datetime.now(),
             price=1, game_has_passed=True, is_full_complite=True, time_duration=40)
        Game.objects.create(quest=partner_3_quest, employee=employee3, date_start=datetime.datetime.now(),
             price=1, game_has_passed=True, is_full_complite=True, time_duration=40)

    def test_success(self):
        count_partners = Partner.task2()
        print(count_partners)
        self.assertEqual(count_partners[0][0], 'a')

class TestTaskThree(TestCase):
    def setUp(self):
        partner = Partner.objects.create(name="partner_for_legend")
        legend = Legend.objects.create(partner=partner, legend="legend_name_1")
        
        partner_1 = Partner.objects.create(name="partner_name_1")
        partner_1_location = Location.objects.create(partner=partner_1, city_name="city_1", metro="metro_1")
        partner_1_quest = Quest.objects.create(legend=legend, location=partner_1_location, name="quest_1")
        employee1 = Employee.objects.create(first_name="name1", last_name="some_name", gender=False)
        Game.objects.create(
            quest=partner_1_quest, employee=employee1, date_start=datetime.datetime(2024, 1, 1),
            price=1, game_has_passed=True, is_full_complite=True, time_duration=20
        )
        Game.objects.create(
            quest=partner_1_quest, employee=employee1, date_start=datetime.datetime(2024, 2, 1),
            price=1, game_has_passed=True, is_full_complite=True, time_duration=20
        )

        partner_2 = Partner.objects.create(name="b")
        partner_2_location = Location.objects.create(partner=partner_2, city_name="city_1", metro="metro_1")
        partner_2_quest = Quest.objects.create(legend=legend, location=partner_2_location, name="quest_2")
        employee2 = Employee.objects.create(first_name="name2", last_name="some_name", gender=True)
        Game.objects.create(
            quest=partner_2_quest, employee=employee2, date_start=datetime.datetime(2024, 1, 1),
            price=1, game_has_passed=True, is_full_complite=True, time_duration=40
        )
        Game.objects.create(
            quest=partner_2_quest, employee=employee2, date_start=datetime.datetime(2024, 2, 1),
            price=1, game_has_passed=True, is_full_complite=True, time_duration=0
        )
    
        partner_3 = Partner.objects.create(name="a")
        partner_3_location = Location.objects.create(partner=partner_3, city_name="city_1", metro="metro_1")
        partner_3_quest = Quest.objects.create(legend=legend, location=partner_3_location, name="quest_3")
        employee3 = Employee.objects.create(first_name="name3", last_name="some_name", gender=True)
        Game.objects.create(quest=partner_3_quest, employee=employee3, date_start=datetime.datetime.now(),
             price=1, game_has_passed=False, is_full_complite=True, time_duration=40)
        Game.objects.create(quest=partner_3_quest, employee=employee3, date_start=datetime.datetime.now(),
             price=1, game_has_passed=False, is_full_complite=True, time_duration=40)
    
    def test_success(self):
            beast_quest = Quest.task3()[0][0]
            print(beast_quest)
            self.assertEqual(beast_quest, "quest_2")
