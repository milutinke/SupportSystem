from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Ticket, TicketAnswers

User = get_user_model()


# Custom pretraga u admin panelu po emailu
class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']

    class Meta:
        model = User


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Ticket)
admin.site.register(TicketAnswers)
