from django.urls import path, include
from django.conf.urls.static import static

from testsite import settings
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('send_mails/', send_mails, name='send_mails'),
    # path('cat/<int:category_id>/', get_category, name='category'),
    path('cat/<int:category_id>/', NewsByCategory.as_view(extra_context={'title': 'Какой-то title'}), name='category'),
    # path('news/<int:news_id>/', view_news, name='view_news'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    # path('news/add-news/', add_news, name='add_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
    path('news/recommended/', RecommendedNews.as_view(), name='recommended_news'),
 ]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
