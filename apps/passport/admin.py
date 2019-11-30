from django.contrib import admin
from django.forms import ModelForm

from .models import Passport


class PassportForm(ModelForm):
    class Meta:
        model = Passport
        fields = '__all__'


class PassportFormAdmin(admin.ModelAdmin):
    form = PassportForm
    list_display = ['creator', 'name', 'secret', 'created_at']


admin.site.register(Passport, PassportFormAdmin)
