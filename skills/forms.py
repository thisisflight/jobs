from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Tag, TagValue


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


class TagValueForm(ModelForm):
    class Meta:
        model = TagValue
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tag'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super(TagValueForm, self).clean()
        title = cleaned_data.get('title').title()
        tag_title = cleaned_data.get('tag')
        tag = Tag.objects.get(title=tag_title)
        queryset = TagValue.objects.filter(title__iexact=title.lower(), tag=tag).exists()
        if queryset:
            raise ValidationError('Такое сочетание тега и значения уже есть')
        return cleaned_data
