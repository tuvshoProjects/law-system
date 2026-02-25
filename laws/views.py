from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import difflib
from .models import Law, LawVersion, Bookmark, ActivityLog


# ======================================
# 1️⃣ Law List
# ======================================
def law_list(request):
    query = request.GET.get("q")
    category = request.GET.get("category")

    laws = Law.objects.all().order_by("title")

    if query:
        laws = laws.filter(
            Q(title__icontains=query) |
            Q(versions__content__icontains=query)
        ).distinct()

    if category:
        laws = laws.filter(category=category)

    categories = Law.objects.values_list("category", flat=True).distinct()

    paginator = Paginator(laws, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "laws/law_list.html", {
        "page_obj": page_obj,
        "categories": categories,
        "query": query
    })


# ======================================
# 2️⃣ Law Detail
# ======================================
def law_detail(request, id):
    law = get_object_or_404(Law, id=id)

    current_version = law.versions.order_by("-effective_date").first()

    context = {
        "law": law,
        "current_version": current_version,
        "versions": law.versions.order_by("-effective_date"),
        "is_editor": request.user.groups.filter(name="Editor").exists()
    }

    return render(request, "laws/law_detail.html", context)


# ======================================
# 3️⃣ Add Version (Editor only)
# ======================================
@login_required
def add_version(request, id):
    law = get_object_or_404(Law, id=id)

    if not request.user.groups.filter(name="editor").exists():
        return redirect("law_detail", id=id)

    if request.method == "POST":
        content = request.POST.get("content")
        effective_date = request.POST.get("effective_date")

        LawVersion.objects.create(
            law=law,
            content=content,
            effective_date=effective_date
        )

        ActivityLog.objects.create(
            user=request.user,
            action=f"{law.title} - шинэ хувилбар нэмсэн"
        )

        return redirect("law_detail", id=id)

    return render(request, "laws/add_version.html", {
        "law": law
    })


# ======================================
# 4️⃣ Version Compare
# ======================================
@login_required
def compare_versions(request, law_id):
    law = get_object_or_404(Law, id=law_id)
    versions = law.versions.order_by("-effective_date")

    v1_id = request.GET.get("v1")
    v2_id = request.GET.get("v2")

    diff_html = None

    if v1_id and v2_id:
        v1 = get_object_or_404(LawVersion, id=v1_id)
        v2 = get_object_or_404(LawVersion, id=v2_id)

        if v1.id != v2.id:
            differ = difflib.HtmlDiff()
            diff_html = differ.make_table(
                v1.content.splitlines(),
                v2.content.splitlines(),
                fromdesc="Old Version",
                todesc="New Version"
            )
            diff_html = mark_safe(diff_html)
        else:
            diff_html = "<div class='alert alert-warning'>Ижил хувилбар сонгосон байна.</div>"

    return render(request, "laws/compare_versions.html", {
        "law": law,
        "versions": versions,
        "diff_html": diff_html
    })


# ======================================
# 5️⃣ Bookmark
# ======================================
@login_required
def add_bookmark(request, id):
    law = get_object_or_404(Law, id=id)

    Bookmark.objects.get_or_create(
        user=request.user,
        law=law
    )

    ActivityLog.objects.create(
        user=request.user,
        action=f"{law.title} - bookmark хийсэн"
    )

    return redirect("law_detail", id=id)


@login_required
def my_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user)

    return render(request, "laws/bookmarks.html", {
        "bookmarks": bookmarks
    })


# ======================================
# 6️⃣ Activity Logs
# ======================================
@login_required
def activity_logs(request):
    logs = ActivityLog.objects.all()

    return render(request, "laws/activity_logs.html", {
        "logs": logs
    })