from django import forms
from django.contrib.auth import get_user_model
from .models import Post
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'text',
            'group'
        )
        labels = {
            'text': _('Текст поста'),
            'group': _('Группа')
        }
        help_texts = {
            'text': _('Напишите что-нибудь здесь!')
        }
        error_messages = {
            'text': {
                'required_field': _('Это обязательное поле!')
            }
        }
