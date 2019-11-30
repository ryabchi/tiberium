from django.db.models import Manager


class ActiveObjectManager(Manager):
    def get_queryset(self):
        return super(ActiveObjectManager, self).get_queryset().filter(is_active=True)


class SystemUserObjectManager(Manager):
    def get_queryset(self):
        queryset = super(SystemUserObjectManager, self).get_queryset()
        result = queryset.filter(is_active=True, is_system=True)
        return result
