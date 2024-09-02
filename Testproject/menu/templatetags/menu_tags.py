from django import template
from menu.models import Menu, MenuItem

register = template.Library()

@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path

    try:
        menu = Menu.objects.prefetch_related('items').get(name=menu_name)
    except Menu.DoesNotExist:
        return {'menu_items': []}

    menu_items = build_tree(menu.items.all(), current_url)
    return {'menu_items': menu_items, 'current_url': current_url}

def build_tree(menu_items, current_url):
    tree = []
    item_dict = {item.id: item for item in menu_items}

    for item in menu_items:
        item.is_active = current_url.startswith(item.get_url())
        if item.parent_id:
            parent = item_dict[item.parent_id]
            if not hasattr(parent, 'children'):
                parent.children = []
            parent.children.append(item)
        else:
            tree.append(item)
    return tree