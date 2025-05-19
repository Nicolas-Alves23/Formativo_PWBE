from django.db import models
from django.core.validators import RegexValidator
# gettext_lazy utilizado para somente trocar o campo 'verbose_name' para somente '_' 💾
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser # Utilizando o modelo pronto de usuário na onde os seguintes itens já são solicitados
"""
1 - Nome do usuário (username)
2 - Primeiro nome (first_name)
3 - Ultimo nome (last_name)
4 - Email (email)
5 - Organização (is_staff)
6 - Se a conta está ativada (is_active)
7 - A data que se juntou (date_joined)

(Para acessar todas as informações CRTL + CLICK🖱)
"""

# Utilizando o validator para validar se o usuário vai colocar o telefone corretamente 
telefone_validator = RegexValidator(
    regex=r'^\+?[\d\s\-\(\)]{10,20}$',
    message="Informe um número de telefone válido."
)

# Utilizando o AbstractUser para criar um usuário, o usuário professor que será manipulado somente pelo Gestor
class Usuario(AbstractUser):
    TIPO_CHOICES = [
        ('G', 'Gestor'),
        ('P', 'Professor')
    ]

    # No Projeto existem dois tipos de usuários Gestor e Professor. O Gestor pode fazer absolutamente tudo(Criar, deletar, modificar)
    # O Professor pode visualizar certas coisas no código

    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, default='P')
    ni = models.PositiveIntegerField(_("Número de identificação"), unique=True)
    # Utilizando o validators criado logo acima
    telefone = models.CharField(_("Número de telefone padrão '(xx)xxxxx-xxxx'"),
        max_length= 30,
        validators=[telefone_validator],
        help_text="O número deve ser passado neste modelo (xx)xxxxx-xxxx"
    )
    
    data_contratacao = models.DateField(_("Data de contratação"))
    data_nascimento = models.DateField(_("A data de nascimento do usuário"))

    REQUIRED_FIELDS = ['ni', 'data_contratacao', 'data_nascimento']

    def __str__(self):
        return f'{self.username} ({self.get_tipo_display()})'

class Disciplina(models.Model):
    nome = models.CharField(_("Nome da discilplina, ex:'Fisíca' "),max_length=255)
    curso = models.CharField(_("Qual curso essa matéria está?"),max_length=255)
    carga_horario = models.PositiveIntegerField(_("Quantas horas da matéria"), default=100)
    descricao = models.TextField(_("Sobre a matéria"))
    # Uma Disciplique tem como chave estrangeira professor
    professor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null= True, blank= True, limit_choices_to={'tipo':'P'},verbose_name=_("Professor que ministra essa disciplina"))
    
    def __str__(self):
        return self.nome

# Sala criada para ser utilizada no 'Reserva_ambiente'
class Sala(models.Model):
    # A validação se o nome é igual a algum dentro do banco de dados é feita no serializers também 
    nome = models.CharField(_("Nome da sala, ex: 'sala verde'"),max_length=90)
    tamanho = models.PositiveIntegerField()
    capacidade = models.PositiveIntegerField(default=50)

    def __str__(self):
        return self.nome

# Modelo de banco de dados para a reserva de ambiente que conecta todas as informações
class Reserva_ambiente(models.Model):
    # A validação dessa área foi feita no serializers
    '''
        A data de início tem que ser menor que a data de término,
        ou seja
        if data['data_inicio'] > data['data_termino']:
            ERROOOOOO
    '''
    data_inicio = models.DateField()
    data_termino = models.DateField()
    
    escolha_horario = (
        ('M', 'Manhã'),
        ('T', 'Tarde'),
        ('N', 'Noite')
    )

    periodo = models.CharField(max_length=1, choices=escolha_horario)
    
    # Chaves estrangeiras
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, verbose_name=_("Escolha a sala da Palestra:"))
    professor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null= True, blank= True, limit_choices_to={'tipo':'P'},verbose_name=_("Escolha qual Professor:"))
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE,verbose_name=_("A Disciplina:"))