

from django.views.generic import ListView, DetailView

from django.shortcuts import render, get_object_or_404

from .models import Post, Comment, Category
from .forms import CommentForm


# ------------------------------------

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.contrib import messages

# --------------------------------------


# Vistas desde la home
class HomeView(ListView):
    template_name = 'nucleo/home.html'
    queryset = Post.objects.all()
    paginate_by = 6 #Cantidad de articulos en la home

    


# Vistas, detalles de los posts
class PostView(DetailView):
    model = Post
    template_name = 'nucleo/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Dado que nuestro campo slug no es único, necesitamos la clave principal para obtener una publicación única
        pk = self.kwargs['pk']
        slug = self.kwargs['slug']

        form = CommentForm()
        post = get_object_or_404(Post, pk=pk, slug=slug)
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post = Post.objects.filter(id=self.kwargs['pk'])[0]
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']

            comment = Comment.objects.create(
                name=name, email=email, content=content, post=post
            )

            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)




class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "image", "tags"]

    def get_success_url(self):
        messages.success(
            self.request, 'Tu publicación ha sido creada con éxito')
        return reverse_lazy("nucleo:home")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.slug = slugify(form.cleaned_data['title'])
        obj.save()
        return super().form_valid(form)




class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "content", "image", "tags"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update = True
        context['update'] = update

        return context

    def get_success_url(self):
        messages.success(
            self.request, 'Tu publicación se ha actualizado correctamente.')
        return reverse_lazy("nucleo:home")

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)




class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post

    def get_success_url(self):
        messages.success(
            self.request, 'Tu publicación ha sido eliminada con éxito.')
        return reverse_lazy("nucleo:home")

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


# Categorias vistas

class CatListView(ListView):
    template_name = 'category.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {
            'cat': self.kwargs['category'],
            'posts': Post.objects.filter(category__name=self.kwargs['category']).filter(status='published')
        }
        return content


def category_list(request):
    category_list = Category.objects.exclude(name='default')
    context = {
        "category_list": category_list,
    }
    return context