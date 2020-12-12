from . import views
from django.urls import path


urlpatterns = [
    path('', views.post_list, name='home'),
    path('post_detail/<slug:_slug>/', views.post_detail, name='post_detail'),
    path('about/', views.blogger_list, name='about'),
    path('post_create/<user>/', views.post_create , name='post_create'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('user_posts/<user>/', views.user_posts, name='user_posts'),
    path('post_delete/<user>/<post_id>',views.post_delete,name='post_delete'),
    path('post_edit/<user>/<post_id>', views.post_edit, name='post_edit'),
    path('contact/', views.contact_message, name='contact'),
    path('user_messages/<user>/', views.user_messages, name='user_messages'),
    path('message_detail/<user>/<message_id>/', views.message_detail, name='message_detail'),
    path('message_delete/<user>/<message_id>',views.message_delete,name='message_delete'),
    path('message_mark_as_read/<user>/<message_id>',views.message_markread,name='message_markread'),
    path('message_forward/<user>/<message_id>',views.message_forward,name='message_forward'),
    # path('message_reply/<user>/<message_id>/', views.message_reply, name='message_reply'),
]
