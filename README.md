# Eventex
Sistema de Eventos criado no curso avançado Welcome To The Django
Exemplo disponível em: https://eventex-rodrigoddc.herokuapp.com/

### Requisitos mínimos:
- git
- heroku
- python versão >= 3.5

## Como clonar e rodar o projeto na sua máquina?
1. Clone o repositório
   - `git clone git@github.com:rodrigoddc/wttd.git`
   - `cd wttd`
2. Crie um ambiente virtual
   - `python3 -m venv .venv`
3. Ative o ambiente virtual
   - unix `source .venv/bin/activate`
   - windows `.\venv\Scripts\activate`
4. Instale as dependências
   - `pip install -r requirements.txt`
5. Configure a instância com o .env-sample
   - `cp contrib/env-sample .env `
6. Execute os testes
   - `python manage.py test`
7. Passados os testes com sucesso, rode o servidor
   - `python manage.py runserver`
8. Abra o navegador e acesso o projeto no endereço
   - `localhost:8000` ou `127.0.0.1:8000`
   
*sugestão: para facilitar seu desenvolvimento. usar o alias no seu perfil/terminal padrão, ex:
- unix:
  - `alias='python $VIRTUAL_ENV/../manage.py'`

- windows:<br/>
    - `echo > wttd/.venv/Scripts/manage.bat`
    - insira no arquivo criado acima `@python "%VIRTUAL_ENV%\..\manage.py" %*` 

## Como fazer o deploy?
1.  Crie uma instância no heroku
    - `heroku create minha_instância`
2. Defina uma SECRET_KEY para instância 
   - à partir do django shell 
     - `django.core.management.utils.get_random_secret_key()`
   - `heroku config:set SECRET_KEY=copie_e_cole_do_valor_gerado_acima`
3. Defina o DEBUG=False
    - `heroku config:set DEBUG=False`
4. Configure o serviço de email
   - preencha os dados em .env como desejar
5. Envie o código para o heroku
    - `git push heroku`

Be happy =]
