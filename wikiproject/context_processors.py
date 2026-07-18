from blog.models import Page

def menu_pages(request):
    return {
        "menu_pages": Page.objects.filter(
            main_menu__gt=0, status="published"
        ).order_by("main_menu")
    }