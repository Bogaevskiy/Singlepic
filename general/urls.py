from django.urls import path
from .views import *

urlpatterns = [    
    path('', landing, name = "landing_url"),
    path('pics_list', PicsList.as_view(), name = "pics_list_url"),
    path('new_user', NewUser.as_view(), name = "new_user_url"),
    path('login', LoginUser.as_view(), name = "user_login_url"),
    path('logout', user_logout, name = "user_logout_url"),
    path('photo_upload', PhotoUpload.as_view(), name = "photo_upload_url"),
    path('user/<str:username>', UserDetail.as_view(), name = "user_detail_url"),
    path('user/<str:username>/delete', UserDelete.as_view(), name = "user_delete_url" ),
    path('users_list', UserList.as_view(), name = "users_list_url"),
    path('pics/<int:id>', PicDetail.as_view(), name = "pic_detail_url"),
    path('pics/<int:id>/delete', PicDelete.as_view(), name = "pic_delete_url"),    
    path('pics/<int:id>/like', photo_like, name = "photo_like_url"),
    path('pics/<int:id>/dislike', photo_dislike, name = "photo_dislike_url"),
    path('user/<str:username>/edit', UserEdit.as_view(), name = "user_edit_url"),
    path('user/<str:username>/base_edit', UserBaseEdit.as_view(), name = "user_base_edit_url"),
    path('about', about, name = 'about_url'),

    path('pics/<int:id>/admin_delete_pic', admin_delete_pic, name = 'admin_delete_pic_url'),
    path('pics/<int:id>/admin_block_pic', admin_block_pic, name = 'admin_block_pic_url'),
    path('user/<str:username>/admin_delete_user', admin_delete_user, name = 'admin_delete_user_url'),
    path('admin_users_list', AdminUsersList.as_view(), name = 'admin_users_list_url'),
    path('admin_pics_list', AdminPicsList.as_view(), name = 'admin_pics_list_url'),
    path('admin_comments_list', AdminCommentsList.as_view(), name = 'admin_comments_list_url'),
    path('pics/<int:pic_id>/admin_block_comment/<int:comm_id>', admin_block_comment, name = 'admin_block_comment'),
    path('pics/<int:pic_id>/admin_delete_comment/<int:comm_id>', admin_delete_comment, name = 'admin_delete_comment'),
    
    path('user/<str:username>/subscribe', user_subscribe, name = 'user_subscribe_url'),
    path('user/<str:username>/unsubscribe', user_unsubscribe, name = 'user_unsubscribe_url'),

    path('user/<str:username>/verify_user', verify_user ,name = 'verify_user_url'),
    path('user/<str:username>/verify/<str:token>', verified_user ,name = 'verified_url'),

    path('subscriptions_list', subscriptions_list, name = 'subscriptions_list_url'),
    path('subs_pics_list', subs_pics_list, name = 'subs_pics_list_url'),
    path('notifications', notifications, name = 'notifications_url'),
    path('restore_access', RestoreAccess.as_view(), name = 'restore_access_url'),
]
