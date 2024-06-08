# CAREER STATUS

## O que é?

O **Career Status** é um sistema de gerenciamento de carreira focado na base, projetado para acompanhar o potencial máximo e mínimo de um jogador, além de adicionar estatísticas e monitorar sua evolução ao longo do tempo.

Infelizmente, o processo é **manual**, então lembre-se de adicionar as estatísticas antes do início da temporada.

## Como executar?

### Pré-requisitos
- Python 3 instalado
- Git instalado
- Ambiente virtual 

### Passo a Passo

1. Clone o projeto na sua pasta que ficará o projeto!

    ```bash
    git clone https://github.com/PedroSawczuk/Career-Status.git
    ```

2. Abra o diretório do projeto no VS Code e acesse o terminal.

3. Crie e ative um ambiente virtual:

    ```bash
    py -m venv venv
    venv\Scripts\activate
    ```

4. Instale as dependências listadas no arquivo **requirements.txt**:

    ```bash
    pip install -r requirements.txt
    ```

5. Configure o banco de dados em **careerstatus/settings.py**.

   **Nota:** Se ainda não criou seu banco de dados, o script **Scripts/createDatabase.py** contém instruções para criar.

6. Após configurar o banco de dados, execute as migrações para criar as tabelas:

    ```bash
    py manage.py makemigrations
    py manage.py migrate
    ```

7. Crie um superusuário:

    ```bash
    py manage.py createsuperuser
    ```

8. Inicie o servidor:

    ```bash
    py manage.py runserver
    ```

Com isso, o sistema estará pronto para uso. Acesse-o pelo navegador e gerencie as carreiras dos jogadores de forma eficiente e organizada.
