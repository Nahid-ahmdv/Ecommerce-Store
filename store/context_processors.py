from .models import Category


def categories(request):
    return {
        'categories': Category.objects.all() #we're gonna collect all the categories in 'Category' table.
    }

#context_processors allowed us to run code throughout the whole of the project.
#by creativing this file, we replaced the previous line in 'context_processors' in settings.py with 'store.context_processors.categories' just to make it look like the other lines there.