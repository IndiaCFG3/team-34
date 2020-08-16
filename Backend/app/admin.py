from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import OperationManager, Mobilizer, Students, Event, CustomToken


admin.site.register(OperationManager)
admin.site.register(Mobilizer)
admin.site.register(Students)
admin.site.register(Event)
admin.site.register(CustomToken)
