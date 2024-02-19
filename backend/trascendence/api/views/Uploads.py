import os

from django.views.decorators.http import require_http_methods
from trascendence.middleware.auth import authorize
from trascendence.settings import BASE_DIR
from trascendence.api.models.User import UserModel
from trascendence.api.models.Uploads import Uploads
from django.http import HttpRequest, JsonResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound
from django import forms
import uuid

UPLOAD_DIR = BASE_DIR / "media"


class FileForm(forms.Form):
    file = forms.FileField()


def save_file_with_user(user: UserModel, file) -> str | None:
    extension = file.name.split('.')[-1]
    new_filename = str(uuid.uuid4()) + "." + extension
    with open(UPLOAD_DIR / new_filename, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)
    Uploads.objects.create(extension=extension, name=new_filename, owner_id=user.id)
    return new_filename


@require_http_methods(['POST'])
@authorize
def upload_file(request: HttpRequest):
    form = FileForm(request.POST, request.FILES)
    auth_info = getattr(request, "auth_info", None)
    if auth_info is None:
        return HttpResponseForbidden(str({"message": "You have no permission to do this."}),
                                     content_type="application/json")
    try:
        user = UserModel.objects.get(username=auth_info['sub'])
    except:
        return HttpResponseForbidden(str({"message": "You have no permission to do this."}),
                                     content_type="application/json")
    if form.is_valid():
        saved_name = save_file_with_user(user, request.FILES['file'])
        if saved_name is not None:
            return JsonResponse({"file": saved_name}, status=200)
    return HttpResponseForbidden(str({"message": "You have no permission to do this."}),
                                 content_type="application/json")


@require_http_methods(['DELETE'])
@authorize
def delete_file(request: HttpRequest, file: str):
    auth_info = getattr(request, "auth_info", None)
    if auth_info is None:
        return HttpResponseForbidden(str({"message": "You have no permission to do this."}),
                                     content_type="application/json")
    try:
        user = UserModel.objects.get(username=auth_info['sub'])
    except:
        return HttpResponseForbidden(str({"message": "You have no permission to do this."}),
                                     content_type="application/json")
    extension = file.split('.')[-1]
    file_name = file[:file.find(extension) - 1]
    try:
        uploaded_file = Uploads.objects.get(name__exact=file_name, extension__exact=extension, owner__exact=user.id)
        os.remove(UPLOAD_DIR / (uploaded_file.name + '.' + uploaded_file.extension))
        uploaded_file.delete()
    except:
        return HttpResponseNotFound(str({"message": "You have no such file."}), content_type="application/json")
