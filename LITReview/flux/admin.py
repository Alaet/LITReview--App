from django.contrib import admin
from django.contrib.auth import get_user_model
from flux.models import Review, Ticket

admin.site.register(get_user_model())
admin.site.register(Review)
admin.site.register(Ticket)
