from django.urls import path
from .views import BlogView, BlogDetailView, AddBlogView, UpdateBlogView, DeleteBlogView
urlpatterns = [
    path('', BlogView.as_view(), name="blog"),
    path('blog_detail/<int:pk>', BlogDetailView.as_view(), name='blog_detail'),
    path('add_blog/', AddBlogView.as_view(), name='add_blog'),
    path('blog_detail/edit/<int:pk>',
         UpdateBlogView.as_view(), name='update_blog'),
    path('blog_detail/<int:pk>/remove',
         DeleteBlogView.as_view(), name='delete_blog'),
]
