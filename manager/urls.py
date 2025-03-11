import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from manager import settings
import manager
from task_manager.views import LoginView, LogoutView, SignUpView, IndexView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("", IndexView.as_view(), name="index"),
    path("", include("task_manager.urls")),
]


if manager.settings.dev.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + static(manager.settings.dev.STATIC_URL, document_root=manager.settings.dev.STATIC_ROOT)
