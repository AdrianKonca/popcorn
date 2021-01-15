import json

from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, reverse
from django.utils import timezone
from django.views import generic

from .forms import RecipeForm, CommentForm, EmailChangeForm
from .models import Recipe, Category, Comment


def index(request):
    return render(request, 'popcorn/main_page.html',
                  {
                      'lastweek': Recipe.objects.get_lastweek(),
                      'recipes': Recipe.objects.get_best_recipes(),
                      'proposed': Recipe.objects.get_proposed()
                  })


def recipe(request):
    return render(request, 'popcorn/recipe.html')


class RecipeView(generic.DetailView):
    model = Recipe
    template_name = 'popcorn/recipe.html'


class CategoriesView(generic.ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'popcorn/categories.html'


def edit_recipe(request, slug=None):
    # TODO: Automatically attach time category
    if not request.user.is_authenticated:
        return render(request, 'popcorn/unauthorized.html')

    if slug is None:
        recipe = None
    else:
        recipe = get_object_or_404(Recipe, slug=slug)

        if request.user != recipe.author and not request.user.is_superuser:
            return render(request, 'popcorn/unauthorized.html')

    if request.method == 'POST':
        form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)
        if form.is_valid():
            if form.instance.author is None:
                form.instance.author = request.user
            form.save()
            return HttpResponseRedirect(reverse("recipe", kwargs={'slug': form.instance.slug}))
    else:
        form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)

    return render(request, 'popcorn/recipe_edit.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'popcorn/logout_success.html')


def vote_recipe(request, slug):
    recipe = Recipe.objects.get(slug=slug)
    user = request.user

    if not user.is_authenticated:
        return render(request, 'popcorn/unauthorized.html')

    vote = recipe.votes.get(user.id)
    body = json.loads(request.body)
    action_string = body['action']
    action_result = action_string
    action_value = recipe.ACTIONS[action_string]

    if vote is not None and vote.action == action_value:
        action_result = recipe.NONE_ACTION
        recipe.votes.delete(user.id)
    else:
        recipe.votes.vote(user.id, action_value)

    recipe = Recipe.objects.get(slug=slug)
    return JsonResponse({'action': action_result, 'count': recipe.vote_score})


def vote_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    user = request.user

    if not user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    vote = comment.votes.get(user.id)
    body = json.loads(request.body)
    action_string = body['action']
    action_result = action_string
    action_value = comment.ACTIONS[action_string]

    if vote is not None and vote.action == action_value:
        action_result = comment.NONE_ACTION
        comment.votes.delete(user.id)
    else:
        comment.votes.vote(user.id, action_value)

    comment = Comment.objects.get(pk=pk)
    return JsonResponse({'action': action_result, 'count': comment.vote_score})


def post_comment(request, slug):
    template_name = 'popcorn/recipe.html'
    recipe = get_object_or_404(Recipe, slug=slug)
    # Todo add check for deleted comments
    # comments = recipe.comments.filter(active=True)
    comments = recipe.comments.all()
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return render(request, 'popcorn/unauthorized.html')
            # return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.recipe = recipe
            if new_comment.author is None:
                new_comment.author = request.user
            # Save the comment to the database
            new_comment.save()
            # Add upvote for the comment from the creater.
            new_comment.votes.vote(request.user.id, new_comment.ACTIONS['up'])
            return HttpResponseRedirect(reverse("recipe", kwargs={'slug': slug}))
    else:
        if not request.user.is_authenticated:
            comment_form = None
        else:
            comment_form = CommentForm()

    comments = zip(
        comments,
        [c.get_vote_status(request.user) for c in comments]
    )

    return render(request, template_name, {'recipe': recipe,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form,
                                           'vote_status': recipe.get_vote_status(request.user)})


def userpage(request):
    user = request.user

    if not user.is_authenticated:
        return render(request, 'popcorn/unauthorized.html')

    return render(request, 'popcorn/user_page.html', {'user': user, 'user_recipes': Recipe.objects.filter(author=user),
                                                      'user_days_from_registration': (
                                                              timezone.now() - user.date_joined).days})


def email_change(request):
    if not request.user.is_authenticated:
        return render(request, 'popcorn/unauthorized.html')

    form = EmailChangeForm(request.user)
    if request.method == 'POST':
        form = EmailChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/accounts/profile/")
    return render(request, 'registration/change_email.html', {'form': form})


def category_viev(request, i=None):
    return render(request, 'popcorn/category.html', {'recipes': Recipe.objects.filter(categories=i)})
