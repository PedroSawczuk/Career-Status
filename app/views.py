from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import *
from django.views.generic import ListView
from django.db.models import Count, Avg, FloatField, ExpressionWrapper, Sum
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
        # Filtra jogadores que não foram vendidos
        return Jogador.objects.filter(vendido=False)
    
class MarcarJogadorVendidoView(View):
    def post(self, request, pk, *args, **kwargs):
        jogador = get_object_or_404(Jogador, pk=pk)
        jogador.vendido = True
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

class AdicionarEstatisticasView(CreateView):
    model = Estatistica
    fields = ['temporada', 'gols', 'assistencias', 'jogos']
    template_name = 'time/adicionarEstatisticas.html'

    def get_success_url(self):
        return reverse_lazy('ver_jogador', kwargs={'pk': self.kwargs['pk']})  # Redireciona para a página do jogador

    def form_valid(self, form):
        jogador = Jogador.objects.get(pk=self.kwargs['pk'])
        form.instance.jogador = jogador
        return super().form_valid(form)

class EditarEstatisticasView(UpdateView):
    model = Estatistica
    fields = ['temporada', 'gols', 'assistencias', 'jogos']
    template_name = 'time/editarEstatisticas.html'

    def get_success_url(self):
        return reverse_lazy('ver_jogador', kwargs={'pk': self.object.jogador.pk})

class EstatisticasView(ListView):
    template_name = 'time/estatisticas.html'
    context_object_name = 'estatisticas'

    def get_queryset(self):
        top_gols = Estatistica.objects.values('jogador__nome').annotate(total_gols=Sum('gols')).order_by('-total_gols')[:10]
        top_assistencias = Estatistica.objects.values('jogador__nome').annotate(total_assistencias=Sum('assistencias')).order_by('-total_assistencias')[:10]
        top_jogos = Estatistica.objects.values('jogador__nome').annotate(total_jogos=Sum('jogos')).order_by('-total_jogos')[:10]

        top_media_participacao = Estatistica.objects.values('jogador__nome').annotate(
            media_participacao=ExpressionWrapper(
                (Sum('gols') + Sum('assistencias')) / Sum('jogos'),
                output_field=FloatField()
            )
        ).order_by('-media_participacao')[:10]

        top_potenciais_nacionalidades = Jogador.objects.values('nacionalidade').annotate(potencial_medio=Avg('potencial_max')).order_by('-potencial_medio')[:10]
        piores_potenciais_nacionalidades = Jogador.objects.values('nacionalidade').annotate(potencial_medio=Avg('potencial_max')).order_by('potencial_medio')[:10]

        jogadores_por_temporada = Jogador.objects.values('temporada_subida').annotate(total=Count('id')).order_by('temporada_subida')
        media_potencial = Jogador.objects.aggregate(media_potencial_min=Avg('potencial_min'), media_potencial_max=Avg('potencial_max'))
        jogadores_por_posicao = Jogador.objects.values('posicao').annotate(total=Count('id')).order_by('-total')
        paises_com_mais_jogadores = Jogador.objects.values('nacionalidade').annotate(total=Count('id')).order_by('-total')[:10]

        return {
            'top_gols': top_gols,
            'top_assistencias': top_assistencias,
            'top_jogos': top_jogos,
            'top_media_participacao': top_media_participacao,
            'top_potenciais_nacionalidades': top_potenciais_nacionalidades,
            'piores_potenciais_nacionalidades': piores_potenciais_nacionalidades,
            'jogadores_por_temporada': jogadores_por_temporada,
            'media_potencial': media_potencial,
            'jogadores_por_posicao': jogadores_por_posicao,
            'paises_com_mais_jogadores': paises_com_mais_jogadores
        }

class ExcluirJogadorView(DeleteView):
    model = Jogador
    template_name = 'time/excluirJogador.html'  
    success_url = reverse_lazy('jogadores_vendidos')