from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Law


def law_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    laws = Law.objects.all()

    # Search
    if query:
        laws = laws.filter(title__icontains=query)

    # Category filter
    if category:
        laws = laws.filter(category=category)

    # Unique categories for dropdown
    categories = Law.objects.values_list('category', flat=True).distinct()

    # Pagination
    paginator = Paginator(laws, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'laws/law_list.html', {
        'page_obj': page_obj,
        'categories': categories,
    })


def law_detail(request, id):
    law = get_object_or_404(Law, id=id)
    return render(request, 'laws/law_detail.html', {'law': law})

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Bookmark


@login_required
def add_bookmark(request, id):
    law = get_object_or_404(Law, id=id)
    Bookmark.objects.get_or_create(user=request.user, law=law)
    return redirect('law_detail', id=id)


@login_required
def my_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request, 'laws/bookmarks.html', {'bookmarks': bookmarks})