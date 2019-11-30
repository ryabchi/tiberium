from django.contrib import admin
from django.contrib.admin.forms import forms
from django.forms import ModelForm

from .models import Like, Post


class PostForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 20}), required=False)
    youtube_link = forms.CharField(max_length=250, help_text='250 characters max.', required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_filter = ('post_type', 'is_active')
    list_display = ['id', 'post_type', 'text', 'youtube_link', 'creator', 'created_at', 'is_active']


admin.site.register(Post, PostAdmin)


class LikeForm(ModelForm):
    class Meta:
        model = Like
        fields = '__all__'


class LikeAdmin(admin.ModelAdmin):
    form = LikeForm
    list_filter = ('creator',)


admin.site.register(Like, LikeAdmin)
