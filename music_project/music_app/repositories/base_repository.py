from django.core.exceptions import ObjectDoesNotExist, FieldError

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return self.model.objects.all()

    def get_by_id(self, id):
        try:
            return self.model.objects.get(pk=id)
        except ObjectDoesNotExist:
            return None

    def add(self, instance):
        instance.save()
        return instance

    def update(self, id, **kwargs):
        obj = self.get_by_id(id)
        if not obj:
            return None
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.save()
        return obj

    def delete(self, id):
        obj = self.get_by_id(id)
        if not obj:
            return False
        obj.delete()
        return True

    def get_by_field(self, field_name, value):
        try:
            return self.model.objects.get(**{field_name: value})
        except (ObjectDoesNotExist, FieldError):
            return None

    def filter_by(self, **kwargs):
        try:
            return self.model.objects.filter(**kwargs)
        except FieldError:
            return self.model.objects.none()
