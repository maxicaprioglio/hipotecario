from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicio, name='index'),
    path('api/cotizacion/', views.obtener_cotizacion_dolar, name='cotizacion_dolar'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('panel/', views.panel_view, name='panel'),
    path('eliminar/<int:consulta_id>/', views.eliminar_consulta, name='eliminar_consulta'),
]