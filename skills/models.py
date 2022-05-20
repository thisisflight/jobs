from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TitleField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        uppercase_list = [x.isupper() for x in str(value)]
        if not any(uppercase_list):
            return str(value).title().strip()
        return str(value)


class Tag(models.Model):
    title = TitleField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class TagValue(models.Model):
    title = TitleField(max_length=50, unique=True)
    user = models.ManyToManyField(User, related_name='values', through='UserTagValue')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class UserTagValue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tagvalues')
    tag_value = models.ForeignKey(TagValue, on_delete=models.CASCADE)
