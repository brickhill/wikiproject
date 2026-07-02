from django.contrib import admin
from django.urls import path, include
from .views import home, register, member, contact
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import MyLoginView, MyLogoutView

handler500 = "wikiproject.views.server_error"
urlpatterns = [
    path('', home, name="home"),
    path('admin/', admin.site.urls),
    path("accounts/login/", MyLoginView.as_view(), name="login"),
    path("accounts/logout/", MyLogoutView.as_view(), name="logout"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path("password_reset/", auth_views.PasswordResetView.as_view(),
         name="password_reset",),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(),
         name="password_reset_done",),
    path("reset/<uidb64>/<token>/",
         auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm",),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(),
         name="password_reset_complete",),
    path("password_change/", auth_views.PasswordChangeView.as_view(),
         name="password_change",),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(),
         name="password_change_done",),
    path('member/', member, name="member"),
    path('blog/', include('blog.urls')),
    path('page/', include('blog.urls')),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path('cookies/', include('cookie_consent.urls')),
    path('contact/', contact, name='contact')
]
if settings.DEBUG:
    (f"Media: {settings.MEDIA_URL}:{settings.MEDIA_ROOT}")
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
