from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.edit import CreateView

from .models import Photo


class HomeListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view displaying home page."""
    model = Photo
    template_name = 'home.html'


class PhotoListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing all photos on site."""
    model = Photo
    template_name = 'photos/photo_list.html'
    paginate_by = 10


class UploadedByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing users photos."""
    model = Photo
    template_name = 'photos/photo_list_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Photo.objects.filter(owner=self.request.user)


class PhotoDetailView(LoginRequiredMixin, generic.DetailView):
    """Generic class-based view displaying a specific photo."""
    template_name = 'photos/photo_detail.html'
    model = Photo


class PhotoCreate(LoginRequiredMixin, CreateView):
    """Generic class-based view, generating form to create new photo object."""
    model = Photo
    template_name = 'photos/photo_form.html'
    fields = ['photo', 'title', 'description']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(PhotoCreate, self).form_valid(form)
