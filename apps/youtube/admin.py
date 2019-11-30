from apps.youtube.models import YoutubeToken
from django.contrib import admin
from django.forms import ModelForm


class YoutubeTokenForm(ModelForm):
    class Meta:
        model = YoutubeToken
        fields = '__all__'


class YoutubeTokenAdmin(admin.ModelAdmin):
    form = YoutubeTokenForm
    list_filter = ('is_active',)


admin.site.register(YoutubeToken, YoutubeTokenAdmin)
