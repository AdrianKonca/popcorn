# Create your tests here.
from django.test import TestCase, Client
from .models import Recipe

from django.utils import timezone
import datetime

from mixer.backend.django import mixer as Mixer
# c = Client()
# response = c.post(reverse(views.edit_recipe), {'name': 'jajo', 'difficulty': 1, "preparation_time" : 5, "servings_count" : 1, "content" : "blablabla"})
# response.status_code

class RecipeManagerTests(TestCase):
    def setUp(self):
        self.user1 = Mixer.blend('popcorn.user')
        self.user2 = Mixer.blend('popcorn.user')
        self.user3 = Mixer.blend('popcorn.user')
        
    def test_lastweek_results_if_enough_recipes(self):
        recipe_lower_limit = Mixer.blend('popcorn.recipe')
        recipe_lower_limit.created_on = timezone.now() - datetime.timedelta(days=6.99)
        recipe_any = Mixer.blend('popcorn.recipe')
        recipe_any.created_on = timezone.now() - datetime.timedelta(days=3)
        recipe_upper_limit = Mixer.blend('popcorn.recipe')
        recipe_upper_limit.created_on = timezone.now()

        lastweek_recipes = list(Recipe.objects.get_lastweek())

        self.assertEqual(len(lastweek_recipes), 3)
        self.assertTrue(recipe_lower_limit in lastweek_recipes)
        self.assertTrue(recipe_any in lastweek_recipes)
        self.assertTrue(recipe_upper_limit in lastweek_recipes)

    def test_get_best_recipes_if_enough_recipes(self):
        recipe_mid = Mixer.blend('popcorn.recipe')
        
        recipe_last = Mixer.blend('popcorn.recipe')
        recipe_last.votes.down(self.user1.id)
        recipe_top = Mixer.blend('popcorn.recipe')
        recipe_top.votes.up(self.user1.id)

        best_recipes = Recipe.objects.get_best_recipes()
        self.assertEqual(len(best_recipes), 3)
        self.assertQuerysetEqual(best_recipes, [recipe_top, recipe_mid, recipe_last], transform=lambda x: x)

    def test_get_proposed_recipes_if_enough_recipes(self):
        recipe_last = Mixer.blend('popcorn.recipe')
        recipe_mid = Mixer.blend('popcorn.recipe')
        recipe_top = Mixer.blend('popcorn.recipe')
        proposed_recipes = Recipe.objects.get_proposed()

        self.assertEqual(len(proposed_recipes), 3)


    def test_lastweek_results_if_not_enough_recipes(self):

        recipe_1 = Mixer.blend('popcorn.recipe')
        recipe_1.created_on = timezone.now() - datetime.timedelta(days=3)
        recipe_1.votes.up(self.user1.id)
        recipe_2 = Mixer.blend('popcorn.recipe')
        recipe_2.created_on = timezone.now() - datetime.timedelta(days=2)
        lastweek_recipes = list(Recipe.objects.get_lastweek())

        self.assertEqual(len(lastweek_recipes), 3)
        self.assertQuerysetEqual(lastweek_recipes, [recipe_1, recipe_2, recipe_1], transform=lambda x: x)

    def test_get_best_recipes_if_not_enough_recipes(self):
        recipe_1 = Mixer.blend('popcorn.recipe')
        recipe_1.votes.up(self.user1.id)
        recipe_2 = Mixer.blend('popcorn.recipe')
        best_recipes = Recipe.objects.get_best_recipes()
        self.assertEqual(len(best_recipes), 3)
        self.assertQuerysetEqual(best_recipes, [recipe_1, recipe_2, recipe_1], transform=lambda x: x)

    def test_get_proposed_recipes_if_not_enough_recipes(self):
        recipe_1 = Mixer.blend('popcorn.recipe')
        recipe_1.name = "aaaa"
        recipe_2 = Mixer.blend('popcorn.recipe')
        recipe_2.name = "bbbb"
        recipe_1.save()
        recipe_2.save()
        proposed_recipes = Recipe.objects.get_proposed()

        self.assertEqual(len(proposed_recipes), 3)
        self.assertQuerysetEqual(proposed_recipes, [recipe_1, recipe_2, recipe_1], transform=lambda x: x)

        def test_get_lastweek_recipes_if_0(self):
            lastweek_recipes = Recipe.objects.get_proposed()
            self.assertEqual(len(lastweek_recipes), 0)

        def test_get_best_recipes_if_0(self):
            best_recipes = Recipe.objects.get_proposed()
            self.assertEqual(len(best_recipes), 0)

        def test_get_proposed_recipes_if_0(self):
            proposed_recipes = Recipe.objects.get_proposed()
            self.assertEqual(len(proposed_recipes), 0)



    def test_return_1(self):
        self.assertEqual(True, True)

class RecipeTests(TestCase):
    def setUp(self):
        self.user1 = Mixer.blend('popcorn.user')
    def test_if_hidden_date_is_set(self):
        recipe = Mixer.blend('popcorn.recipe')
        recipe.hidden_on = timezone.now()
        recipe.save()
        self.assertEqual(recipe.is_hidden(), True)

    def test_if_hidden_date_is_not_set(self):
        recipe = Mixer.blend('popcorn.recipe')
        recipe.save()
        self.assertEqual(recipe.is_hidden(), False)

    def test_if_deleted_date_is_set(self):
        recipe = Mixer.blend('popcorn.recipe')
        recipe.deleted_on = timezone.now()
        recipe.save()
        self.assertEqual(recipe.is_deleted(), True)

    def test_if_deleted_date_is_not_set(self):
        recipe = Mixer.blend('popcorn.recipe')
        recipe.save()
        self.assertEqual(recipe.is_deleted(), False)

    def test_if_recipes_have_diffrent_slug(self):
        recipe_1 = Mixer.blend('popcorn.recipe')
        recipe_1.name = "pizza"
        recipe_2 = Mixer.blend('popcorn.recipe')
        recipe_2.name = "pizza"
        recipe_1.save()
        recipe_2.save()
        self.assertNotEqual(recipe_1.slug, recipe_2.slug)

class VoteTest(TestCase):
    def setUp(self):
        self.user1 = Mixer.blend('popcorn.user')
    def test_get_vote_status_if_up(self):
        recipe = Mixer.blend('popcorn.recipe')
        recipe.votes.up(self.user1.id)

        self.assertEqual(recipe.get_vote_status(self.user1), "up")

    def test_get_vote_status_if_down(self):
        recipe = Mixer.blend('popcorn.recipe')
        recipe.votes.down(self.user1.id)

        self.assertEqual(recipe.get_vote_status(self.user1), "down")

    def test_get_vote_status_if_no_vote(self):
        recipe = Mixer.blend('popcorn.recipe')

        self.assertEqual(recipe.get_vote_status(self.user1), "default")

    