from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/registration/$', views.user_registration, name='user-registration'),
    url(r'^user/login/$', views.user_login, name ='user-login'),
    url(r'^user/logout/$', views.user_logout, name ='user-logout'),
    url(r'^tasks/$', views.TaskListView.as_view(), name='tasks'),
    url(r'^task/(?P<pk>\d+)$', views.TaskDetailView.as_view(), name='task-detail'),
    url(r'^task/(?P<pk>\d+)/delete$', views.task_delete, name='task-delete'),
    url(r'^task/(?P<pk>\d+)/edit$', views.task_edit, name='task-update'),
    url(r'^task/(?P<pk>\d+)/complete$', views.task_complete, name='task-complete'),
    url(r'^task/add/$', views.task_add, name='task-add'),
    url(r'^archive/$', views.ArchiveListView.as_view(), name='archive'),
]