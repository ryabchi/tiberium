from django.db.models import BooleanField, DateTimeField, IntegerField, Manager, Model, TextField
from tiberium.query_manager import ActiveObjectManager


class YoutubeToken(Model):
    token = TextField(null=False)
    count = IntegerField(default=0)
    created_at = DateTimeField(auto_now_add=True, editable=False)
    is_active = BooleanField(default=True)

    objects = Manager()
    active = ActiveObjectManager()

    class Meta:
        verbose_name = "Youtube Token"
        ordering = ('pk',)

    def __str__(self):
        return f'{self.pk}'
