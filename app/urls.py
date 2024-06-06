from django.urls import path

from app.views import *

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path('criar_jogador/', CriarJogadorView.as_view(), name='criar_jogador'),
    path('ver_jogadores/', VerJogadoresView.as_view(), name='ver_jogadores'),
    path('estatisticas/', EstatisticasView.as_view(), name='estatisticas'),
    path('ver_jogador/<int:pk>/', VerJogadorView.as_view(), name='ver_jogador'),
    path('adicionar_estatisticas/<int:pk>/', AdicionarEstatisticasView.as_view(), name='adicionar_estatisticas'),
    path('editar_estatisticas/<int:pk>/', EditarEstatisticasView.as_view(), name='editar_estatisticas'),
]