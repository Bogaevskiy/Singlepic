from django.urls import path
from .views import *

urlpatterns = [    
    path('', PicsList.as_view(), name = "pics_list_url"),
    path('new_user', NewUser.as_view(), name = "new_user_url"),
    path('login', LoginUser.as_view(), name = "user_login_url"),
    path('logout', user_logout, name = "user_logout_url"),
    path('photo_upload', PhotoUpload.as_view(), name = "photo_upload_url"),
    path('user/<str:username>', UserDetail.as_view(), name = "user_detail_url"),
    path('user/<str:username>/delete', UserDelete.as_view(), name = "user_delete_url" ),
    path('users_list', UserList.as_view(), name = "users_list_url"),
    path('pics/<int:id>', PicDetail.as_view(), name = "pic_detail_url"),
    path('pics/<int:id>/delete', PicDelete.as_view(), name = "pic_delete_url"),
    path('user/<str:username>/edit', UserEdit.as_view(), name = "user_edit_url"),
    path('about', about, name = 'about.html'),
    path('pics/<int:id>/admin_delete_pic', admin_delete_pic, name = 'admin_delete_pic_url'),
    path('user/<str:username>/admin_delete_user', admin_delete_user, name = 'admin_delete_user_url'),
    path('admin_users_list', AdminUsersList.as_view(), name = 'admin_users_list_url'),
    path('admin_pics_list', AdminPicsList.as_view(), name = 'admin_pics_list_url')  
]
