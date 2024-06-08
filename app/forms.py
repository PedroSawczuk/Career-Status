from django import forms
from .models import Estatistica

class EstatisticaForm(forms.ModelForm):
    class Meta:
        model = Estatistica
        fields = ['temporada', 'gols', 'assistencias', 'jogos']

    def __init__(self, *args, **kwargs):
        jogador = kwargs.pop('jogador', None)
        super().__init__(*args, **kwargs)
        if jogador:
            temporadas_existentes = Estatistica.objects.filter(jogador=jogador).values_list('temporada', flat=True)
            all_temporadas = [choice for choice in Estatistica.TEMPORADAS_CHOICES if choice[0] not in temporadas_existentes]
            self.fields['temporada'].choices = all_temporadas
