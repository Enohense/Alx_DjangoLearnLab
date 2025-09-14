from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Document


@login_required
@permission_required("content.can_view", raise_exception=True)
def document_list(request):
    # minimal demo
    titles = ", ".join(Document.objects.values_list("title", flat=True))
    return HttpResponse(f"Docs: {titles or 'None'}")


@login_required
@permission_required("content.can_create", raise_exception=True)
def document_create(request):
    if request.method == "POST":
        title = request.POST.get("title") or "Untitled"
        body = request.POST.get("body", "")
        Document.objects.create(title=title, body=body, author=request.user)
        return HttpResponse("Created")
    return HttpResponse("POST a new document")


@login_required
@permission_required("content.can_edit", raise_exception=True)
def document_edit(request, pk: int):
    doc = get_object_or_404(Document, pk=pk)
    if request.method == "POST":
        doc.title = request.POST.get("title", doc.title)
        doc.body = request.POST.get("body", doc.body)
        doc.save()
        return HttpResponse("Edited")
    return HttpResponse(f"Edit form for {doc.title}")


@login_required
@permission_required("content.can_delete", raise_exception=True)
def document_delete(request, pk: int):
    if request.method != "POST":
        return HttpResponseForbidden("Use POST to delete")
    doc = get_object_or_404(Document, pk=pk)
    doc.delete()
    return HttpResponse("Deleted")
