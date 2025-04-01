from django.contrib import admin
from django.urls import path
from .views import model_metadata_view, news_view, UserWatchlistView, allowed_symbols_view, get_watchlist_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/models/', model_metadata_view),
    path('api/news/', news_view),
    path('api/watchlist/', UserWatchlistView.as_view()),
    path('api/allowed-symbols/', allowed_symbols_view),
    path('api/watchlist-live/', get_watchlist_view, name='watchlist-live'),
]
