from django.urls import path
from app.views import *

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path('criar_jogador/', CriarJogadorView.as_view(), name='criar_jogador'),
    path('ver_jogadores/', VerJogadoresView.as_view(), name='ver_jogadores'),
    path('estatisticas/', EstatisticasView.as_view(), name='estatisticas'),
    path('ver_jogador/<int:pk>/', VerJogadorView.as_view(), name='ver_jogador'),
    path('jogador/<int:pk>/vender/', MarcarJogadorVendidoView.as_view(), name='marcar_jogador_vendido'),
    path('adicionar_estatisticas/<int:pk>/', AdicionarEstatisticasView.as_view(), name='adicionar_estatisticas'),
    path('editar_estatisticas/<int:pk>/', EditarEstatisticasView.as_view(), name='editar_estatisticas'),
    path('jogadores_vendidos/', JogadoresVendidosView.as_view(), name='jogadores_vendidos'),
    path('retirar_venda_jogador/<int:pk>/', RetirarVendaJogadorView.as_view(), name='retirar_venda_jogador'),
    path('excluir_jogador/<int:pk>/', ExcluirJogadorView.as_view(), name='excluir_jogador'),
    path('jogadores_por_temporada/', JogadoresPorTemporadaView.as_view(), name='jogadores_por_temporada'),

    path('reset-database/', ResetDatabaseView.as_view(), name='reset_database'),

]