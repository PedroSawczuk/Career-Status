from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import *
from django.views.generic import ListView
from django.db.models import Count, Avg, FloatField, ExpressionWrapper, Sum
from django.views import View
from django.http import JsonResponse
from django.shortcuts import redirect
from django.db import connection
from app.forms import EstatisticaForm
from .models import *

class HomePageView(TemplateView):
    template_name = "home.html"

class CriarJogadorView(CreateView):
    model = Jogador
    fields = ['nome', 'posicao', 'potencial_min', 'potencial_max', 'nacionalidade', 'temporada_subida']
    template_name = 'time/criarJogador.html'
    success_url = reverse_lazy('ver_jogadores')

class VerJogadoresView(ListView):
    model = Jogador
    template_name = 'time/verJogadores.html'
    context_object_name = 'jogadores'

    def get_queryset(self):
        return Jogador.objects.filter(vendido=False).order_by('nome')

class JogadorDeleteView(DeleteView):
    model = Jogador
    template_name = 'time/deleteJogadores.html' 
    success_url = reverse_lazy('ver_jogadores') 
    
class JogadoresPorTemporadaView(TemplateView):
    template_name = 'time/jogadoresPorTemporada.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        temporadas_com_dados = Estatistica.objects.values_list('temporada', flat=True).distinct()

        dados_por_temporada = {}
        for temporada in temporadas_com_dados:
            estatisticas = Estatistica.objects.filter(temporada=temporada)
            jogadores_estatisticas = [
                {
                    'nome': estatistica.jogador.nome,
                    'nacionalidade': estatistica.jogador.get_nacionalidade_display(),
                    'jogos': estatistica.jogos,
                    'gols': estatistica.gols,
                    'assistencias': estatistica.assistencias
                }
                for estatistica in estatisticas
            ]
            dados_por_temporada[temporada] = jogadores_estatisticas

        context['dados_por_temporada'] = dados_por_temporada
        return context

class MarcarJogadorVendidoView(View):
    def post(self, request, pk, *args, **kwargs):
        jogador = get_object_or_404(Jogador, pk=pk)
        jogador.vendido = True
        jogador.save()
        return redirect('ver_jogadores')

class RetirarVendaJogadorView(View):
    def post(self, request, pk):
        jogador = Jogador.objects.get(pk=pk)
        jogador.vendido = False
        jogador.save()
        return redirect('ver_jogadores')

class JogadoresVendidosView(ListView):
    model = Jogador
    template_name = 'time/jogadoresVendidos.html'
    context_object_name = 'jogadores_vendidos'

    def get_queryset(self):
        return Jogador.objects.filter(vendido=True)

class VerJogadorView(DetailView):
    model = Jogador
    template_name = 'time/verJogador.html'
    context_object_name = 'jogador'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jogador = self.object
        estatisticas = jogador.estatisticas.all()

        total_jogos = estatisticas.aggregate(Sum('jogos'))['jogos__sum'] or 0
        total_gols = estatisticas.aggregate(Sum('gols'))['gols__sum'] or 0
        total_assistencias = estatisticas.aggregate(Sum('assistencias'))['assistencias__sum'] or 0
        
        # Calculate average goals per game
        media_gols_por_jogo = total_gols / total_jogos if total_jogos > 0 else 0
        
        # Get the best season for goals and assists
        melhor_temporada_gols = estatisticas.order_by('-gols').first()
        melhor_temporada_assistencias = estatisticas.order_by('-assistencias').first()

        context.update({
            'total_jogos': total_jogos,
            'total_gols': total_gols,
            'total_assistencias': total_assistencias,
            'media_gols_por_jogo': media_gols_por_jogo,
            'melhor_temporada_gols': melhor_temporada_gols,
            'melhor_temporada_assistencias': melhor_temporada_assistencias,
        })

        return context

class AdicionarEstatisticasView(CreateView):
    model = Estatistica
    form_class = EstatisticaForm
    template_name = 'time/adicionarEstatisticas.html'

    def get_success_url(self):
        return reverse_lazy('ver_jogadores')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        jogador = get_object_or_404(Jogador, pk=self.kwargs['pk'])
        kwargs['jogador'] = jogador
        return kwargs

    def form_valid(self, form):
        jogador = get_object_or_404(Jogador, pk=self.kwargs['pk'])
        form.instance.jogador = jogador
        return super().form_valid(form)

class EditarEstatisticasView(UpdateView):
    model = Estatistica
    form_class = EstatisticaForm
    template_name = 'time/editarEstatisticas.html'

    def get_success_url(self):
        return reverse_lazy('ver_jogador', kwargs={'pk': self.object.jogador.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Adiciona o jogador ao contexto do formulário
        kwargs['jogador'] = self.object.jogador
        return kwargs


class EstatisticasView(ListView):
    template_name = 'time/estatisticas.html'
    context_object_name = 'estatisticas'
    queryset = Jogador.objects.all()  # Definindo um queryset aqui, mesmo que não seja usado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        top_gols = Estatistica.objects.values('jogador__nome').annotate(total_gols=Sum('gols')).order_by('-total_gols')[:10]
        top_assistencias = Estatistica.objects.values('jogador__nome').annotate(total_assistencias=Sum('assistencias')).order_by('-total_assistencias')[:10]
        top_jogos = Estatistica.objects.values('jogador__nome').annotate(total_jogos=Sum('jogos')).order_by('-total_jogos')[:10]

        top_media_participacao = Estatistica.objects.values('jogador__nome').annotate(
            media_participacao=ExpressionWrapper(
                (Sum('gols') + Sum('assistencias')) / Sum('jogos'),
                output_field=FloatField()
            )
        ).order_by('-media_participacao')[:10]

        jogadores_por_temporada = Jogador.objects.values('temporada_subida').annotate(total=Count('id')).order_by('temporada_subida')
        media_potencial = Jogador.objects.aggregate(media_potencial_min=Avg('potencial_min'), media_potencial_max=Avg('potencial_max'))
        jogadores_por_posicao = Jogador.objects.values('posicao').annotate(total=Count('id')).order_by('-total')
        paises_com_mais_jogadores = Jogador.objects.values('nacionalidade').annotate(total=Count('id')).order_by('-total')[:10]

        gols_por_posicao = Estatistica.objects.exclude(jogador__posicao='Goleiro').values('jogador__posicao').annotate(total_gols=Sum('gols'))
        gols_por_pais = Estatistica.objects.values('jogador__nacionalidade').annotate(total_gols=Sum('gols'))

        context.update({
            'top_gols': top_gols,
            'top_assistencias': top_assistencias,
            'top_jogos': top_jogos,
            'top_media_participacao': top_media_participacao,
            'jogadores_por_temporada': jogadores_por_temporada,
            'media_potencial': media_potencial,
            'jogadores_por_posicao': jogadores_por_posicao,
            'paises_com_mais_jogadores': paises_com_mais_jogadores,
            'gols_por_posicao': gols_por_posicao,
            'gols_por_pais': gols_por_pais,
        })

        return context

class ExcluirJogadorView(DeleteView):
    model = Jogador
    template_name = 'time/excluirJogador.html'
    success_url = reverse_lazy('jogadores_vendidos')

class ResetDatabaseView(View):
    def post(self, request, *args, **kwargs):
        if request.POST.get('confirm') == 'delete':
            with connection.cursor() as cursor:
                cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')  # Desabilita checagem de chave estrangeira
                cursor.execute('DELETE FROM app_estatistica;')
                cursor.execute('DELETE FROM app_jogador;')
                cursor.execute('DELETE FROM app_nacionalidadeestatistica;')
                cursor.execute('ALTER TABLE app_estatistica AUTO_INCREMENT = 1;')  # Reseta o auto incremento
                cursor.execute('ALTER TABLE app_jogador AUTO_INCREMENT = 1;')  # Reseta o auto incremento
                cursor.execute('ALTER TABLE app_nacionalidadeestatistica AUTO_INCREMENT = 1;')  # Reseta o auto incremento
                cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')  # Reabilita checagem de chave estrangeira

            return redirect('home')  # Redireciona após o reset
        return JsonResponse({'error': 'Confirmação inválida'}, status=400)

class SearchPlayersView(ListView):
    model = Jogador
    template_name = 'time/pesquisaResultados.html'  # Crie este template para exibir os resultados
    context_object_name = 'players'

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Jogador.objects.filter(nome__icontains=query)