from django.db import models


class Operadora(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    logo = models.ImageField(upload_to='operadoras/logos/', null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    data_criacao = models.DateField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome


class TipoServico(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.nome


class DadoEstatistico(models.Model):
    operadora = models.ForeignKey(Operadora, on_delete=models.CASCADE, related_name='dados')
    tipo_servico = models.ForeignKey(TipoServico, on_delete=models.CASCADE)
    data_referencia = models.DateField()
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    observacao = models.TextField(blank=True, null=True)
    data_insercao = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-data_referencia', 'operadora']
        unique_together = ['operadora', 'tipo_servico', 'data_referencia']
    
    def __str__(self):
        return f"{self.operadora.nome} - {self.tipo_servico.nome} - {self.data_referencia}" 