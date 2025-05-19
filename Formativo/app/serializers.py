'''
    Arquivo que é responsavel pela converter das informações para json
    Dentro do arquivo foram feitas certas validações dos inputs do usuário
    Algumas validações feitas no código foram feitas pela primeira vez 
    Foram utilizadas diversas ferramentas inclusive IA's para o auxilio no desenvolvimento
    
'''


# Import do timedelta e datetime para a validação na parte de Reserva de ambientes (verificar se datas)
from datetime import timedelta, datetime
from rest_framework import serializers
# importando os itens do meu models
from .models import Sala, Usuario, Disciplina, Reserva_ambiente
# Biblioteca que utilizo para o uso de Tokens 🔐
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Serializer que é utilizado para manusear as salas
class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = '__all__'
    '''
       Validação mencionada no arquivo models 
       Se nome for igual algum nome dentro do banco
       Mensagem que o usuário recebera vai ser     
       "Não é possível criar uma sala com o mesmo nome." 
    '''
    def validate(self, validated_data):
        
        # Para receber os nomes do banco de dados é necessário faer está linha de código
        nome = validated_data.get('nome')
        
        # Filtrando se nome = nome (se o nome passado é repetido)
        if Sala.objects.filter(nome=nome).exists():
            raise serializers.ValidationError("Não é possível criar uma sala com o mesmo nome.")
        
        return validated_data

# Manipulando Usuário
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Usuario(**validated_data)
        user.set_password(password) 
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = '__all__'


class LoginSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)

        data['user'] = {
            'username': self.user.username,
            'email': self.user.email,
            'tipo': self.user.tipo,
        }
        return data

class ReservaAmbienteSerializer(serializers.ModelSerializer):
    
    repetir = serializers.BooleanField(write_only=True, required=False, default=False)
    repetir_dias = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=6),  
        write_only=True,
        required=False
    )
    repetir_ate = serializers.DateField(write_only=True, required=False)

    class Meta:
        model = Reserva_ambiente
        fields = [
            'data_inicio', 'data_termino', 'periodo',
            'sala', 'professor', 'disciplina',
            'repetir', 'repetir_dias', 'repetir_ate'
        ]

    def validate(self, data):

        if data['data_inicio'] < datetime.today().date():
            raise serializers.ValidationError("A data de início não pode ser anterior à data de hoje.")

        if data['data_inicio'] > data['data_termino']:
            raise serializers.ValidationError("A data de início não pode ser posterior à data de término.")
        

        conflitos = Reserva_ambiente.objects.filter(
            data_inicio__lte=data['data_termino'],
            data_termino__gte=data['data_inicio'],
            sala=data['sala'],
            periodo=data['periodo']
        )


        if self.instance:
            conflitos = conflitos.exclude(pk=self.instance.pk)

        if conflitos.exists():
            raise serializers.ValidationError("Essa sala já está reservada nesse período.")

        return data

    def create(self, validated_data):

        repetir = validated_data.pop('repetir', False)
        repetir_dias = validated_data.pop('repetir_dias', [])
        repetir_ate = validated_data.pop('repetir_ate', None)

        reservas_criadas = []

        def conflito(data, sala, periodo):
            return Reserva_ambiente.objects.filter(
                data_inicio__lte=data,
                data_termino__gte=data,
                sala=sala,
                periodo=periodo
            ).exists()

        sala = validated_data['sala']
        periodo = validated_data['periodo']
        professor = validated_data['professor']
        disciplina = validated_data['disciplina']

        if not repetir:

            for dia in self._daterange(validated_data['data_inicio'], validated_data['data_termino']):
                if conflito(dia, sala, periodo):
                    raise serializers.ValidationError(
                        f"Conflito de reserva no dia {dia.strftime('%d/%m/%Y')} ({periodo})."
                    )

            return Reserva_ambiente.objects.create(**validated_data)

        data_atual = validated_data['data_inicio']
        while data_atual <= repetir_ate:
            if data_atual.weekday() in repetir_dias: 
                if not conflito(data_atual, sala, periodo):
                    reserva = Reserva_ambiente.objects.create(
                        data_inicio=data_atual,
                        data_termino=data_atual,
                        periodo=periodo,
                        sala=sala,
                        professor=professor,
                        disciplina=disciplina
                    )
                    reservas_criadas.append(reserva)
            data_atual += timedelta(days=1)

        if not reservas_criadas:
            raise serializers.ValidationError("Nenhuma reserva foi criada. Todos os dias selecionados estavam com conflitos.")


        return reservas_criadas[0]

    def _daterange(self, start_date, end_date):

        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)

# http://127.0.0.1:8000/admin/app/usuario/add/