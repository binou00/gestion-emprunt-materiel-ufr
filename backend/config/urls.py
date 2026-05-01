"""URL routing principal du projet."""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
    # Authentification (vues built-in Django)
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Admin
    path("admin/", admin.site.urls),

    # API REST (JSON)
    path("api/", include("api.urls")),

    # Bonus : dashboard administrateur + exports CSV
    path("bonus/", include("bonus.urls")),

    # Pages HTML (en dernier car contient la racine "")
    path("", include("pages.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR.parent / "frontend" / "static")
