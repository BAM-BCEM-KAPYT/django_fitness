import os
# import re
from django.shortcuts import render
from django.db.models import F
from homepage.models import Client
from homepage.models import Group

log = ''
clients = Client.objects.in_bulk()
groups = Group.objects.in_bulk()
stay_out_clients = []


def button_choose_group_pressed(request):
    clients_list = Client.objects.filter(group__id=int(request.POST.get("Group")))
    result = '<option value="">Выбирете идентификатор</option>'
    for client in clients_list:
        result += f'<option value="{client.id}">Идентификатор {client.id} - {clients[int(client.id)].fio}</option>'
    return result


def button_choose_person_pressed(request):
    return f'У клиента {clients[int(request.POST.get("ID"))].fio} осталось ' \
           f'{clients[int(request.POST.get("ID"))].classes} занятий.'


def button_extend_classes_pressed(request):
    global log
    if clients[int(request.POST.get("ID"))].classes > 0:
        return f'У клиента {clients[int(request.POST.get("ID"))].fio} ещё есть занятия!'
    else:
        if request.POST.get("classes_number") == '4_classes':
            clients[int(request.POST.get("ID"))].classes = 4
            Client.objects.filter(id=int(request.POST.get("ID"))).update(classes=4)
            log += f'Клиент {clients[int(request.POST.get("ID"))].fio}' \
                   f' - {int(request.POST.get("ID"))}: добавлено 4 занятия\n'
        elif request.POST.get("classes_number") == '8_classes':
            clients[int(request.POST.get("ID"))].classes = 8
            Client.objects.filter(id=int(request.POST.get("ID"))).update(classes=8)
            log += f'Клиент {clients[int(request.POST.get("ID"))].fio}' \
                   f' - {int(request.POST.get("ID"))}: добавлено 8 занятия\n'
        elif request.POST.get("classes_number") == '16_classes':
            clients[int(request.POST.get("ID"))].classes = 16
            Client.objects.filter(id=int(request.POST.get("ID"))).update(classes=16)
            log += f'Клиент {clients[int(request.POST.get("ID"))].fio}' \
                   f' - {int(request.POST.get("ID"))}: добавлено 16 занятия\n'
        return 'Информационное окно'


def button_delete_client_pressed(request):
    global log
    log += f'Клиент {clients[int(request.POST.get("ID"))].fio} - {int(request.POST.get("ID"))}: клиент удален\n'
    Group.objects.filter(id=clients[int(request.POST.get("ID"))].group_id).update(clients_count=F('clients_count') - 1)
    groups[clients[int(request.POST.get("ID"))].group_id].clients_count -= 1
    Client.objects.filter(id=int(request.POST.get("ID"))).delete()
    del clients[int(request.POST.get("ID"))]


def button_new_client_pressed(request):
    global clients, log
    Client.objects.create(fio=request.POST.get("fio"), id=request.POST.get("id"),
                          classes=0, group_id=int(request.POST.get("new_group")))
    Group.objects.filter(id=int(request.POST.get("new_group"))).update(clients_count=F('clients_count') + 1)
    groups[int(request.POST.get("new_group"))].clients_count += 1
    clients = Client.objects.in_bulk()
    log += f'Клиент {clients[int(request.POST.get("id"))].fio} - {int(request.POST.get("id"))}: клиент добавлен\n'


def button_new_group_pressed(request):
    global groups, log
    Group.objects.create(title=request.POST.get("new_group_title"), clients_count=0)
    groups = Group.objects.in_bulk()
    log += f'Группа {request.POST.get("new_group_title")}: группа добавлена\n'


def button_delete_group_pressed(request):
    global log, clients
    log += f'Группа {groups[int(request.POST.get("Group"))].title}: группа удалена\n'
    Group.objects.filter(id=int(request.POST.get("Group"))).delete()
    del groups[int(request.POST.get("Group"))]
    clients = Client.objects.in_bulk()


def button_change_group_pressed(request):
    global log
    client_id = ''
    if request.POST.get("ID_without_group") != '':
        client_id = int(request.POST.get("ID_without_group"))
    elif request.POST.get("ID") != '':
        client_id = int(request.POST.get("ID"))
        Group.objects.filter(id=clients[client_id].group_id).update(clients_count=F('clients_count') - 1)
        groups[clients[client_id].group_id].clients_count -= 1
    log += f'Клиент {clients[client_id].fio} - {client_id}: группа изменена с ' \
        f'{groups[clients[client_id].group_id].title} на {groups[int(request.POST.get("new_change_group"))].title}\n'
    Group.objects.filter(id=request.POST.get("new_change_group")).update(clients_count=F('clients_count') + 1)
    groups[int(request.POST.get("new_change_group"))].clients_count += 1
    Client.objects.filter(id=client_id).update(group_id=request.POST.get("new_change_group"))
    clients[client_id].group_id = int(request.POST.get("new_change_group"))


def button_print_log_pressed(request):
    global log
    if log != '':
        # directory_folder = request.POST.get("folder")
        directory_folder = r"D:\Python projects\Django_test\log.txt"
        if not os.path.exists(os.path.dirname(directory_folder)):
            os.makedirs(os.path.dirname(directory_folder))
        with open(directory_folder, 'a+') as file:
            file.write(log)
        log = ''
        print('log')
        return 'Информационное окно'
    else:
        return 'Пустой лог!'


def index(request):
    info_text = 'Информационное окно'
    clients_list = '<option value="">Выбирете идентификатор</option>'

    if request.method == "POST":
        try:
            if 'new_client' in request.POST:
                button_new_client_pressed(request)
            if 'create_new_group' in request.POST:
                button_new_group_pressed(request)
            if 'delete_group' in request.POST:
                button_delete_group_pressed(request)
            if 'choose_group' in request.POST:
                clients_list = button_choose_group_pressed(request)
            if 'print_log' in request.POST:
                info_text = button_print_log_pressed(request)
        except ValueError:
            info_text = 'Не выбрана группа!'
        except TypeError:
            info_text = 'Не выбрана группа!'
        except KeyError:
            info_text = 'Не выбрана группа!'

        try:
            if 'choose_person' in request.POST:
                info_text = button_choose_person_pressed(request)
            if 'change_group' in request.POST:
                button_change_group_pressed(request)
            if 'delete_client' in request.POST:
                button_delete_client_pressed(request)
            if 'extend_classes' in request.POST:
                info_text = button_extend_classes_pressed(request)
        except ValueError:
            info_text = 'Не выбран идентификатор!'
        except TypeError:
            info_text = 'Не выбран идентификатор!'
        except KeyError:
            info_text = 'Не выбран идентификатор!'

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

    clients_without_group_list = '<option value="">Выбирете идентификатор</option>'
    for id in clients:
        if not clients[id].group_id:
            clients_without_group_list += f'<option value="{id}">Идентификатор {id} - {clients[id].fio}</option>'

    context = {
        'clients_without_group_list': clients_without_group_list,
        'clients_list': clients_list,
        'groups_list': groups_list,
        'info_text': info_text,
    }
    return render(request, 'manager/manager.html', context)
