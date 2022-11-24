import pyperclip
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from fitness_world.common.forms import CommentCreateForm, CommentEditForm, CommentDeleteForm, SearchForm
from fitness_world.common.models import LikePhoto, CommentPhoto
from fitness_world.core.photo_utils import photo_is_liked_by_user, photo_likes_count
from fitness_world.photos.models import Photo


# Tested
def index(request):
    user = request.user

    if not user.is_authenticated:
        return index_no_profile(request)

    search_form = SearchForm(request.GET)
    search_patter = None

    if search_form.is_valid():
        search_patter = search_form.cleaned_data['workout_name']

    photos = Photo.objects.all()

    if search_patter:
        photos = photos.filter(workout__name__icontains=search_patter)

    photos = [photo_likes_count(photo) for photo in photos]
    photos = [photo_is_liked_by_user(request, photo) for photo in photos]

    context = {
        'user': user,
        'photos': photos,
        'comment_form': CommentCreateForm(),
        'search_form': search_form,
    }

    return render(request, 'common/home-page.html', context)


def index_no_profile(request):
    return render(request, 'common/home-page.html')


# Tested
@login_required
def like_photo(request, pk):
    user_liked_photo = LikePhoto.objects.filter(photo_id=pk, user_id=request.user.pk)

    if user_liked_photo:
        user_liked_photo.delete()
    else:
        LikePhoto.objects.create(
            photo_id=pk,
            user_id=request.user.pk,
        )

    url_to_redirect = request.META['HTTP_REFERER'] + f'#photo-{pk}'

    return redirect(url_to_redirect)


@login_required
def create_comment(request, pk):
    photo = Photo.objects.filter(pk=pk).get()

    form = CommentCreateForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.photo = photo
        comment.user = request.user
        comment.save()

    return redirect(request.META['HTTP_REFERER'])


@login_required
def delete_comment(request, pk):
    comment = CommentPhoto.objects.filter(pk=pk).get()
    photo = comment.photo

    if request.method == 'GET':
        form = CommentDeleteForm(instance=comment)
    else:
        form = CommentDeleteForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()
            return redirect('details photo', pk=photo.pk)

    context = {
        'form': form,
        'comment': comment,
    }

    return render(request, 'comments/delete-comment-page.html', context)


class EditCommentView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'comments/edit-comment-page.html'
    model = CommentPhoto
    form_class = CommentEditForm

    def get_success_url(self):
        return reverse_lazy('details photo', kwargs={'pk': self.object.photo.pk})


@login_required
def share_photo(request, pk):
    photo_details_url = request.META['HTTP_HOST'] + reverse_lazy('details photo', kwargs={'pk': pk})

    pyperclip.copy(photo_details_url)

    return redirect(request.META['HTTP_REFERER'] + f'#photo-{pk}')
