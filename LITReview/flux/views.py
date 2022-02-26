from itertools import chain

import django.db.utils
from django.db.models.base import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Value, CharField
from django.shortcuts import render, redirect, get_object_or_404


from flux import models, forms
from authentication.models import User, UserFollow
from flux.models import Review, Ticket


@login_required
def home(request):
    following = UserFollow.objects.filter(user=request.user)
    reviews = Review.objects.all()
    tickets = Ticket.objects.all()
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    user_review = []
    user_ticket_unrated = []
    for item in reviews:
        if item.user == request.user or item.ticket.user == request.user:
            user_review.append(item)
        for user in following:
            if item.user == user.followed_user or item.ticket.user == user.followed_user:
                if item in user_review:
                    pass
                else:
                    user_review.append(item)
    for item in tickets:
        if item.user == request.user:
            if not item.rated:
                user_ticket_unrated.append(item)
        for user in following:
            if not item.rated:
                if item.user == user.followed_user:
                    user_ticket_unrated.append(item)
    posts = sorted(
        chain(user_review, user_ticket_unrated), key=lambda post: post.time_created, reverse=True
    )
    context = {
        'posts': posts,
        'following': following,
    }
    return render(request, 'flux/home.html', context=context)


@login_required
def my_posts(request):
    user_posts = Review.objects.filter(user_id=request.user.id)
    user_tickets = Ticket.objects.filter(user_id=request.user.id)
    context = {
        'user_posts': user_posts,
        'user_tickets': user_tickets,
    }
    return render(request, 'flux/my_posts.html', context=context)


@login_required
def post_new_review(request):
    review_form = forms.ReviewForm()
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        ticket_form = forms.TicketForm(request.POST, request.FILES)

        if all([ticket_form.is_valid(), review_form.is_valid()]):
            tickets = ticket_form.save(commit=False)
            reviews = review_form.save(commit=False)
            reviews.ticket = tickets
            tickets.user = request.user
            tickets.rated = True
            ticket_form.save()
            reviews.user = request.user
            review_form.save()
            return redirect('home')
    context = {
        'review_form': review_form,
        'ticket_form': ticket_form,
    }
    return render(request, 'flux/add_review.html', context=context)


@login_required
def post_ticket_review(request, ticket_id):
    review_form = forms.ReviewForm()

    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            reviews = review_form.save(commit=False)
            ticket.rated = True
            reviews.ticket = ticket
            reviews.user = request.user
            review_form.save()
            ticket.save()
            return redirect('home')
    context = {
        'review_form': review_form,
        'ticket': ticket
    }
    return render(request, 'flux/post_ticket_review.html', context=context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    ticket = review.ticket
    edit_form = forms.ReviewForm(instance=review)
    if request.method == "POST":
        edit_form = forms.ReviewForm(request.POST, instance=review)
        if edit_form.is_valid():
            edit_form.save()
            return redirect("home")
    context = {
        "edit_form": edit_form,
        'item': ticket
    }
    return render(request, "flux/edit_review.html", context=context)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    ticket = get_object_or_404(models.Ticket, id=review.ticket.id)
    delete_form = forms.DeleteReviewForm()
    if request.method == 'POST':
        delete_form = forms.DeleteReviewForm(request.POST)
        if delete_form.is_valid():
            ticket.rated = False
            ticket.save()
            review.delete()
            return redirect('home')
    context = {
        'item': review,
        'delete_form': delete_form,
    }
    return render(request, 'flux/delete_review.html', context=context)


@login_required
def post_ticket(request):
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            photo = ticket_form.save(commit=False)
            ticket_form.image = photo
            ticket_form.instance.user = request.user
            ticket_form.save()
            return redirect('home')
    return render(request, 'flux/post_ticket.html', context={'ticket_form': ticket_form})


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        edit_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('home')
    return render(request, 'flux/edit_ticket.html', context={'edit_form': edit_form})


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    delete_form = forms.DeleteTicketForm()
    if request.method == 'POST':
        delete_form = forms.DeleteTicketForm(request.POST)
        if delete_form.is_valid():
            ticket.delete()
            return redirect('home')
    context = {
        'item': ticket,
        'delete_form': delete_form,
    }
    return render(request, 'flux/delete_ticket.html', context=context)


@login_required()
def user_follow(request):
    user_form = forms.UserFollowsForm()
    following = UserFollow.objects.filter(user=request.user)
    followed_by = UserFollow.objects.filter(followed_user=request.user)

    if request.method == "POST":
        user_form = forms.UserFollowsForm(request.POST)

        username = request.POST["username_follow"]
        try:
            user = User.objects.get(username=username)

            if user_form.is_valid() and user and user != request.user:
                try:
                    UserFollow.objects.create(user=request.user, followed_user=user)
                    return redirect("follow-users")
                except django.db.utils.IntegrityError:
                    ...
        except ObjectDoesNotExist:
            ...
    if len(following) == 0 or len(followed_by) == 0:
        message = "On dirait qu'il n'y a personne ..."
    else:
        message = None
    context = {
        "following": following,
        "followed_by": followed_by,
        "form": user_form,
        "message": message
    }
    return render(
        request,
        "flux/follow_users_form.html",
        context=context,
    )


@login_required
def delete_user_follows(request, followed_user_id=None):
    user = get_object_or_404(User, id=followed_user_id)
    follow = get_object_or_404(UserFollow, user=request.user, followed_user=user)

    if follow:
        follow.delete()
    return redirect("follow-users")
