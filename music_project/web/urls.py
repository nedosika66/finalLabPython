from django.urls import path
from django.contrib.auth import views as auth_views

from web.views import songs, artists, analytics, tech, general

urlpatterns = [
    path('', general.home, name='home'),

    path('songs/', songs.song_list, name='song_list'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='web/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('song/<int:pk>/', songs.song_detail, name='song_detail'),
    path('song/create/', songs.song_edit, name='song_create'),
    path('song/<int:pk>/edit/', songs.song_edit, name='song_edit'),
    path('song/<int:pk>/delete/', songs.song_delete, name='song_delete'),

    path('artist/<int:pk>/', artists.artist_detail, name='artist_detail'),
    path('artists/', artists.artist_list, name='artist_list'),

    path('dashboard/', analytics.dashboard, name='dashboard'),
    path('dashboard/v2/', analytics.dashboard_bokeh, name='dashboard_bokeh'),
    path('dashboard/api/', analytics.dashboard_api, name='dashboard_api'),
    path('dashboard/export/', analytics.export_dashboard_csv, name='dashboard_export'),

    path('external-api/', tech.external_api_view, name='external_data'),
    path('performance/', tech.performance_dashboard, name='performance'),
]