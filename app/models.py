from django.db import models

class Jogador(models.Model):

    POSICOES_CHOICES = (
        ("GOL", "Goleiro"),
        ("LD", "Lateral Direito"),
        ("LE", "Lateral Esquerdo"),
        ("ZAG", "Zagueiro"),
        ("VOL", "Volante"),
        ("MC", "Meio-Campista Central"),
        ("ME", "Meia Esquerda"),
        ("MD", "Meia Direita"),
        ("MEI", "Meia Atacante"),
        ("PD", "Ponta Direita"),
        ("PE", "Ponta Esquerda"),
        ("ATA", "Atacante"),
        ("SA", "Segundo Atacante"),
    )

    TEMPORADAS_CHOICES = (
        ("2018/19", "2018/19"),
        ("2019/20", "2019/20"),
        ("2020/21", "2020/21"),
        ("2021/22", "2021/22"),
        ("2022/23", "2022/23"),
        ("2023/24", "2023/24"),
        ("2024/25", "2024/25"),
        ("2025/26", "2025/26"),
        ("2026/27", "2026/27"),
        ("2027/28", "2027/28"),
        ("2028/29", "2028/29"),
        ("2029/30", "2029/30"),
        ("2030/31", "2030/31"),
    )

    PAISES_CHOICES = (
        ("BRA", "Brasil"),
        ("ARG", "Argentina"),
        ("NLD", "Holanda"),
        ("FRA", "França"),
        ("BEL", "Bélgica"),
        ("CHE", "Suíça"),
        ("AUT", "Áustria"),
        ("DNK", "Dinamarca"),
        ("GBR", "Inglaterra"),
        ("FIN", "Finlândia"),
        ("IRL", "Irlanda"),
        ("NIR", "Irlanda do Norte"),
        ("NOR", "Noruega"),
        ("RUS", "Rússia"),
        ("SCO", "Escócia"),
        ("SWE", "Suécia"),
        ("HRV", "Croácia"),
        ("GRC", "Grécia"),
        ("PRT", "Portugal"),
        ("ITA", "Itália"),
        ("ESP", "Espanha"),
        ("TUR", "Turquia"),
        ("CZE", "República Tcheca"),
        ("POL", "Polônia"),
        ("ROU", "Romênia"),
        ("SVK", "Eslováquia"),
        ("SVN", "Eslovênia"),
        ("SRB", "Sérvia"),
        ("CHN", "China"),
        ("JPN", "Japão"),
        ("KOR", "Coreia do Sul"),
        ("SAU", "Arábia Saudita"),
        ("AUS", "Austrália"),
        ("NZL", "Nova Zelândia"),
        ("CAN", "Canadá"),
        ("MEX", "México"),
        ("USA", "Estados Unidos"),
        ("BOL", "Bolívia"),
        ("CHL", "Chile"),
        ("COL", "Colômbia"),
        ("ECU", "Equador"),
        ("PRY", "Paraguai"),
        ("PER", "Peru"),
        ("URY", "Uruguai"),
        ("VEN", "Venezuela"),
        ("DZA", "Argélia"),
        ("CMR", "Camarões"),
        ("EGY", "Egito"),
        ("GHA", "Gana"),
        ("CIV", "Costa do Marfim"),
        ("MAR", "Marrocos"),
        ("NGA", "Nigéria"),
        ("ZAF", "África do Sul"),
    )


    id = models.AutoField(primary_key=True)  
    nome = models.CharField(max_length=100)
    posicao = models.CharField(max_length=3, choices=POSICOES_CHOICES)
    potencial_min = models.PositiveIntegerField()
    potencial_max = models.PositiveIntegerField()
    nacionalidade = models.CharField(max_length=3, choices=PAISES_CHOICES)
    temporada_subida = models.CharField(max_length=7, choices=TEMPORADAS_CHOICES)

    def __str__(self):
        return self.nome

class Estatistica(models.Model):
    TEMPORADAS_CHOICES = (
        ("2018/19", "2018/19"),
        ("2019/20", "2019/20"),
        ("2020/21", "2020/21"),
        ("2021/22", "2021/22"),
        ("2022/23", "2022/23"),
        ("2023/24", "2023/24"),
        ("2024/25", "2024/25"),
        ("2025/26", "2025/26"),
        ("2026/27", "2026/27"),
        ("2027/28", "2027/28"),
        ("2028/29", "2028/29"),
        ("2029/30", "2029/30"),
        ("2030/31", "2030/31"),
    )

    id = models.AutoField(primary_key=True)
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE, related_name='estatisticas') 
    temporada = models.CharField(max_length=7, choices=TEMPORADAS_CHOICES)
    jogos = models.PositiveIntegerField(default=0)
    gols = models.PositiveIntegerField(default=0)
    assistencias = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.jogador} - {self.temporada}"

class JogadorVendido(models.Model):
    jogador = models.OneToOneField(Jogador, on_delete=models.CASCADE, primary_key=True)  # Relacionamento 1-1 com Jogador
    valor_venda = models.PositiveIntegerField()  # Valor da venda
    temporada_venda = models.CharField(max_length=7, choices=Estatistica.TEMPORADAS_CHOICES)  # Temporada da venda

    def save(self, *args, **kwargs):
        # Impede a criação de estatísticas após a venda
        if self.jogador.estatisticas.filter(temporada__gte=self.temporada_venda).exists():
            raise ValueError("Não é possível adicionar estatísticas após a venda do jogador.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.jogador} - Vendido por {self.valor_venda} na temporada {self.temporada_venda}"
