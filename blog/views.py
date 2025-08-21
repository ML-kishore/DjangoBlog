from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView,CreateView,DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post

def about(request):
    return render(request,'blog/about.html',{'title':'About'})

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5  # two posts per page

class PostDetailView(DetailView): # done mistake by not changing deaitlview to listview
    model = Post
    
class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user #form you are tyring to submit make that instance author = current logged user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user #form you are tyring to submit make that instance author = current logged user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
            
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView): 
    model = Post
    success_url = '/'

    #this tests the user who is gonna delete the post is post owner or logged user
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


def home(request):
    context = {'posts':Post.objects.all()}
    return render(request,'blog/home.html',context)