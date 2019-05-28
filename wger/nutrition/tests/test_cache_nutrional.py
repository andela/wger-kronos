from wger.core.tests.base_testcase import WorkoutManagerTestCase
from wger.core.models import Language
from django.contrib.auth.models import User
from django.core.cache import cache
from wger.utils.cache import cache_mapper
from wger.nutrition.models import NutritionPlan, Meal, MealItem


class CacheNutritionalPlanTestCase(WorkoutManagerTestCase):

    @classmethod
    def create_nutrition_data(self):
        nutrition_plan = NutritionPlan()
        nutrition_plan.user = User.objects.create_user(username='reifred')
        nutrition_plan.language = Language.objects.get(short_name="en")
        nutrition_plan.save()

        meal = Meal()
        meal.plan = nutrition_plan
        meal.order = 1
        meal.save()

        meal_item = MealItem()
        meal_item.meal = meal
        meal_item.amount = 1
        meal_item.ingredient_id = 1
        meal_item.order = 1

        return [nutrition_plan, meal, meal_item]

    def test_presence_of_cache_data_without_setting_nutritional_plan_in_cache(self):
        nutritional_plan = self.create_nutrition_data()[0]
        self.assertFalse(
            cache.get(cache_mapper.get_nutritional_value_plan(nutritional_plan)))

    def test_presence_of_cache_data_after_setting_nutritional_plan_in_cache(self):
        nutritional_plan = self.create_nutrition_data()[0]
        self.assertFalse(
            cache.get(cache_mapper.get_nutritional_value_plan(nutritional_plan)))
        nutritional_plan.get_nutritional_values()
        self.assertTrue(
            cache.get(cache_mapper.get_nutritional_value_plan(nutritional_plan)))

    def test_cache_key_deletion_on_save_of_a_nutritional_plan(self):
        nutritional_plan = self.create_nutrition_data()[0]
        nutritional_plan.get_nutritional_values()
        self.assertTrue(cache.get(cache_mapper.get_nutritional_value_plan(nutritional_plan)))
        nutritional_plan.save()
        self.assertFalse(cache.get(cache_mapper.get_nutritional_value_plan(nutritional_plan)))

    def test_cache_key_deletion_on_delete_of_a_nutritional_plan(self):
        nutritional_plan = self.create_nutrition_data()[0]
        nutritional_plan.get_nutritional_values()
        self.assertTrue(cache.get(cache_mapper.get_nutritional_value_plan(nutritional_plan)))
        nutritional_plan.delete()
        self.assertFalse(cache.get(cache_mapper.get_nutritional_value_plan(nutritional_plan)))

    def test_cache_key_deletion_on_save_of_a_meal(self):
        nutrition_data = self.create_nutrition_data()
        nutritional_plan = nutrition_data[0]
        meal = nutrition_data[1]
        nutritional_plan.get_nutritional_values()
        self.assertTrue(cache.get(cache_mapper.get_nutritional_value_plan(nutritional_plan)))
        meal.save()
        self.assertFalse(
            cache.get(cache_mapper.get_nutritional_value_plan(nutritional_plan)))

    def test_cache_key_deletion_on_delete_of_a_meal(self):
        nutrition_data = self.create_nutrition_data()
        nutritional_plan = nutrition_data[0]
        meal = nutrition_data[1]
        nutritional_plan.get_nutritional_values()
        self.assertTrue(cache.get(cache_mapper.get_nutritional_value_plan(nutritional_plan)))
        meal.delete()
        self.assertFalse(
            cache.get(cache_mapper.get_nutritional_value_plan(nutritional_plan)))

    def test_cache_key_deletion_on_save_of_a_meal_item(self):
        nutrition_data = self.create_nutrition_data()
        nutritional_plan = nutrition_data[0]
        meal_item = nutrition_data[2]
        nutritional_plan.get_nutritional_values()
        self.assertTrue(cache.get(cache_mapper.get_nutritional_value_plan(nutritional_plan)))
        meal_item.save()
        self.assertFalse(
            cache.get(cache_mapper.get_nutritional_value_plan(nutritional_plan)))
