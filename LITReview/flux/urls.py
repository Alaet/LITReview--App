from django.urls import path
from flux import views as flux_views

urlpatterns = [
    path('home/', flux_views.home, name='home'),
    path('add_review/', flux_views.post_new_review, name='add-new-review'),
    path('edit_review/<int:review_id>/', flux_views.edit_review, name='edit-review'),
    path('delete_review/<int:review_id>/', flux_views.delete_review, name='delete-review'),
    path('ask_review/', flux_views.post_ticket, name='post-ticket'),
    path('post_ticket_review/<int:ticket_id>/', flux_views.post_ticket_review, name='post-ticket-review'),
    path('my_posts/', flux_views.my_posts, name='my-posts'),
    path('my_posts/<int:ticket_id>/edit/', flux_views.edit_ticket, name='edit-ticket'),
    path('my_posts/<int:ticket_id>/delete/', flux_views.delete_ticket, name='delete-ticket'),
    path('follow-users/', flux_views.user_follow, name='follow-users'),
    path('<int:followed_user_id>/', flux_views.delete_user_follows, name='delete-user-follow'),
]
