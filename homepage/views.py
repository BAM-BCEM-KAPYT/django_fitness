from django.shortcuts import render
from django.db.models import F
from .models import Client
from .models import Group
from manager import views

clients = Client.objects.in_bulk()
groups = Group.objects.in_bulk()
stay_out_clients = []


def switch(arg):
    return {
        1: "занятие",
        2: "занятия",
        3: "занятия",
        4: "занятия",
        5: "занятий",
        6: "занятий",
        7: "занятий",
        8: "занятий",
        9: "занятий",
        0: "занятий",
    }[arg]


def button_choose_group_pressed(request):
    clients_list = Client.objects.filter(group__id=int(request.POST.get("Group")))
    result = '<option value="">Выбирете идентификатор</option>'
    for client in clients_list:
        result += f'<option value="{client.id}">Идентификатор {client.id} - {clients[int(client.id)].fio}</option>'
    return result


def button_choose_person_pressed(request):
    return f'У клиента {clients[int(request.POST.get("ID"))].fio} - {int(request.POST.get("ID"))} осталось ' \
           f'{clients[int(request.POST.get("ID"))].classes}' \
           f' {switch(clients[int(request.POST.get("ID"))].classes % 10)}.'


def button_class_pressed(request):
    log = f'Занятие в группе {groups[int(request.POST.get("Group"))].title}'
    if request.POST.get('all_here') == 'on':
        log += ', присутствуют все'
    result = ''
    clients_list = Client.objects.filter(group__id=int(request.POST.get("Group")))
    for client in clients_list:
        if client.classes > 0:
            if request.POST.get('all_here') == 'on' or stay_out_clients.count(client.id) == 0:
                clients[client.id].classes -= 1
                Client.objects.filter(id=client.id).update(classes=F('classes') - 1)
            else:
                log += f', отсутствует клиент {client.fio} - {client.id}'
        else:
            result += f'У клиента {client.fio} не осталось занятий! '
    if result == '':
        result = 'Информационное окно'
    log += '\n'
    views.log += log
    return result


def button_stay_out_pressed(request):
    views.log += f'Клиент {clients[int(request.POST.get("ID"))].fio}' \
                 f' - {int(request.POST.get("ID"))}: клиент отсутствует\n'
    stay_out_clients.append(clients[int(request.POST.get("ID"))].id)


def index(request):
    info_text = 'Информационное окно'
    clients_list = '<option value="">Выбирете идентификатор</option>'

    if request.method == "POST":
        if 'class' in request.POST:
            info_text = button_class_pressed(request)
        try:
            if 'choose_person' in request.POST:
                info_text = button_choose_person_pressed(request)
            if 'stay_out' in request.POST:
                button_stay_out_pressed(request)
        except ValueError:
            info_text = 'Не выбран идентификатор!'
        except TypeError:
            info_text = 'Не выбрана группа!'

        try:

            if 'choose_group' in request.POST:
                clients_list = button_choose_group_pressed(request)
        except ValueError:
            info_text = 'Не выбрана группа!'

    groups_list = ''
    if request.POST.get("Group") and "delete_group" not in request.POST:
        groups_list = f'<option value="{int(request.POST.get("Group"))}">' \
                      f'{groups[int(request.POST.get("Group"))].title} ' \
                      f'- {groups[int(request.POST.get("Group"))].clients_count}</option>'
        groups_list += '<option value="">Выбирете группу</option>'
        for id in groups:
            if id != int(request.POST.get("Group")):
                groups_list += f'<option value="{id}">{groups[id].title} - {groups[id].clients_count}</option>'
        clients_list = button_choose_group_pressed(request)
    else:
        groups_list += '<option value="">Выбирете группу</option>'
        for id in groups:
            groups_list += f'<option value="{id}">{groups[id].title} - {groups[id].clients_count}</option>'

    context = {
        'clients_list': clients_list,
        'groups_list': groups_list,
        'info_text': info_text,
    }
    return render(request, 'homepage/homepage.html', context)
