from django.urls import path
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(),name='index'),
    #<int:pk>に投稿のIDが入る
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    #新規投稿用のURLを作成する
    path('post/new/', views.CreatePostView.as_view(),name='post_new'),
    # 投稿の編集用のURLを作成する
    path('post/<int:pk>/edit/',views.PostEditView.as_view(),name='post_edit'),
    # 投稿の削除用のURLを作成する
    path('post/<int:pk>/delete/',views.PostDeleteView.as_view(),name='post_delete'),
    # カテゴリー用のURLを作成する
    path('category/<str:category>/', views.CategoryView.as_view(), name='category'),
    # 検索用のURLを作成
    path('search/',views.SearchView.as_view(),name='search')
    
] 