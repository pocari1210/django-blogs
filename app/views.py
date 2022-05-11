from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Post,Category
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q
from functools import reduce
from operator import and_

class IndexView(View):
    def get(self,request,*args,**kwargs):
        
        # objects.order_by():降順に並び変える
        post_data=Post.objects.order_by("-id")

        # render関数:テンプレートにデータを渡す
        return render(request,"app/index.html",{
            'post_data':post_data,
        })

class PostDetailView(View):
    def get(self,request,*args,**kwargs):

        # IDでモデルデータのフィルターをかけて、データを取得する
        post_data=Post.objects.get(id=self.kwargs['pk'])

        # 取得したデータをテンプレートに渡す
        return render(request,'app/post_detail.html',{
            'post_data': post_data
        })

class CreatePostView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        
        return render(request, 'app/post_form.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post()
            post_data.author = request.user
            post_data.title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            category_data = Category.objects.get(name=category)
            post_data.category = category_data
            post_data.content = form.cleaned_data['content']
            post_data.save()
            return redirect('post_detail', post_data.id)

        return render(request, 'app/post_form.html', {
            'form': form
        })

class PostEditView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        post_data=Post.objects.get(id=self.kwargs['pk'])
        form = PostForm(
            request.POST or None,
            initial={
                'title':post_data.title,
                'category': post_data.category,
                'content':post_data.content,
            }
        )
        
        return render(request, 'app/post_form.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post.objects.get(id=self.kwargs['pk'])
            post_data.title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            category_data = Category.objects.get(name=category)
            post_data.category = category_data
            post_data.content = form.cleaned_data['content']
            post_data.save()
            return redirect('post_detail', self.kwargs['pk'])

        return render(request, 'app/post_form.html', {
            'form': form
        })

class PostDeleteView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_delete.html', {
            'post_data':post_data
        })

    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('index')

class CategoryView(View):
    def get(self, request, *args, **kwargs):
        category_data = Category.objects.get(name=self.kwargs['category'])
        post_data = Post.objects.order_by('-id').filter(category=category_data)
        return render(request, 'app/index.html', {
            'post_data': post_data
        })

class SearchView(View):
    def get(self,request,*args,**kwargs):
        post_data=Post.objects.order_by('-id')
        keyword=request.GET.get('keyword')

        if keyword:
            exclution_list=[' ','　']

            query_list=''
            for word in keyword:
                if not word in exclution_list:
                    query_list+=word
            
            query = reduce(and_, [Q(title__icontains=q) | Q(content__icontains=q) for q in query_list])
            post_data=post_data.filter(query)
        
        return render(request,'app/index.html',{
            'keyword':keyword,
            'post_data':post_data,
        })

