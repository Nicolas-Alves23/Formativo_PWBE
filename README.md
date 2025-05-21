# Formativo_PWBE

O projeto visa o desenvolvimento de um sistema de gerenciamento de professores, disciplinas e reservas de ambientes, utilizando Django e Django Rest Framework. O sistema permitirá que gestores cadastrem, visualizem, atualizem e excluam informações sobre professores, disciplinas e reservas de salas, enquanto os professores terão acesso restrito à visualização das disciplinas a que estão atribuídos e das reservas de salas. O projeto inclui a implementação de autenticação e autorização, garantindo que apenas os gestores possam realizar ações de CRUD, enquanto os professores terão acesso apenas a informações pertinentes às suas atividades. Além disso, o sistema terá endpoints de CRUD para todas as entidades, mecanismos de validação, e será integrado a um banco de dados MySQL.

## Começando o projeto 
Para ser utilizada a aplicação é preciso fazer algumas checagens e completar os seguintes passos.
1. Verifique se o Python está instalado da maneira correta.
2. Faça um servidor local.
~~~
python -m venv nome-servidor
nome-servidor/Scripts/server # Ativando o servidor
~~~
3. Instalar as dependências `requiments.txt` com o comando `pip install -r requiments.txt`.
4. Após todos esses passos verifique se sua maquina contém o Mysql Workbench instalado corretamente.
5. Depois verificar no `settings.py` do projeto se as configurações do database estão corretas.
~~~
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cadastro',
        'USER': 'root',
        'PASSWORD': 'senai',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}
~~~
6. Como desfecho rode a aplicação com o comando `python manage.py runserver`
