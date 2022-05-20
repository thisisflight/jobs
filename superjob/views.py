from django.contrib.auth import get_user_model
from django.shortcuts import render

from utils.process_values import get_values_data

User = get_user_model()


def index_page(request):
    users = User.objects.prefetch_related('values__tag', 'tagvalues')
    users_data = {}
    for user in users:
        users_data[user.username] = get_values_data(user.values.all())
    context = {'users': users, 'users_data': users_data}
    return render(request, 'index.html', context)
