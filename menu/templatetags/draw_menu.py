from django import template
from django.utils.datastructures import MultiValueDictKeyError

from menu.models import MenuItem

register = template.Library()


@register.inclusion_tag('menu/draw_menu.html', takes_context=True)
def draw_menu(context, menu) -> dict:
    menu_items = MenuItem.objects.filter(menu__title=menu)
    item_values = menu_items.values()
    parents = [item for item in item_values.filter(parent=None)]
    try:
        selected_item = menu_items.get(id=context['request'].GET[menu])
        expanded_items_id_list = get_expanded_items_id_list(selected_item)
        for parent in parents:
            if parent['id'] in expanded_items_id_list:
                parent['child_items'] = get_child_items(
                    item_values, parent['id'], expanded_items_id_list
                )
        result = {'items': parents}
    except MultiValueDictKeyError:
        result = {'items': parents}
    result['menu'] = menu
    return result


def get_expanded_items_id_list(parent):
    expanded_items_id_list = []
    while parent:
        expanded_items_id_list.append(parent.id)
        parent = parent.parent
    return expanded_items_id_list


def get_child_items(item_values, current_parent_id, expanded_items_id_list):
    current_parent_child_list = [
        item for item in item_values.filter(parent_id=current_parent_id)
    ]
    for child in current_parent_child_list:
        if child['id'] in expanded_items_id_list:
            child['child_items'] = get_child_items(
                item_values, child['id'], expanded_items_id_list
            )
    return current_parent_child_list
