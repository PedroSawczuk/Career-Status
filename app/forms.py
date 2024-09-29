# app/forms.py
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
            # Filtra apenas as temporadas que já foram adicionadas
            self.fields['temporada'].choices = [choice for choice in Estatistica.TEMPORADAS_CHOICES if choice[0] in temporadas_existentes]