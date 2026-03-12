from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('completed/', views.completed_tasks, name='completed_tasks'),
    path('create/', views.create_task, name='create_task'),
    path('update/<int:pk>/', views.update_task, name='update_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('update-priority/', views.update_priority, name='update_priority'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('activity-log/', views.activity_log, name='activity_log'),
    path('task/<int:pk>/complete/', views.complete_task, name='complete_task'),
    path('task/<int:pk>/mark_pending/', views.mark_task_pending, name='mark_task_pending'),
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="reset/password_reset.html",
        email_template_name="reset/password_reset_email.html",
        subject_template_name="reset/password_reset_subject.txt",
    ), name="password_reset"),

    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(
        template_name="reset/password_reset_done.html"
    ), name="password_reset_done"),

    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="reset/password_reset_confirm.html"
    ), name="password_reset_confirm"),

    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="reset/password_reset_complete.html"
    ), name="password_reset_complete"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('overdue/', views.overdue_tasks, name='overdue_tasks'),
]