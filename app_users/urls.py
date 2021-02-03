from django.urls import path

from .views import AnotherLoginView, AnotherLogoutView, register_view, Account, AccountEditFormView

urlpatterns = [
    path('login/', AnotherLoginView.as_view(), name='login'),
    path('logout/', AnotherLogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('account/<int:pk>/', Account.as_view(), name='account'),
    path('account/<int:pk>/edit/', AccountEditFormView.as_view(), name='edit')
]
