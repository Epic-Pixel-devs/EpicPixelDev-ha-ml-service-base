# ha-ml-service-base

### Instalação e Configuração de Ambiente

- Fazer download Python 3.7
  [download here](https://www.python.org/downloads/) compatível com Tensorflow versão 2.11 https://www.tensorflow.org/install/
- Fazer download do gitbash: [download here](https://git-scm.com/)
- Fazer clone do projeto no
  github: [clone here](https://github.com/Epic-Pixel-devs/ha-ml-service-base): `git clone https://github.com/Epic-Pixel-devs/ha-ml-service-base`
- Entrar no diretório e criar ambiente: `cd ha-ml-service-base`
- Criar novo Ambiente Virtual: `python -m venv .venv`
- Fazer update do pip:
  - windows: `.venv\Script\Activate` e `pip install pip --upgrade`
    > obs: caso ocorra error de script no power shell deverá fazer
    > a permissão. Rodar este comando como admin  
    > `Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser`
  - Linux: `source .venv/bin/activate` e `pip install pip --upgrade`
- Fazer a instalação das dependências: `python py_ignore_requirements.py`
- Fazer a inclusão das variáveis de ambiente.
- Roder o projeto local: `flask run`

### Help - Guia para fazer Unit Test

- https://docs.mongoengine.org/guide/mongomock.html
- https://realpython.com/python-mock-library/
- https://docs.python.org/3/library/unittest.mock-examples.html
- https://www.datacamp.com/tutorial/pytest-tutorial-a-hands-on-guide-to-unit-testing
- https://dev.to/yamakanto/how-i-set-up-vscode-for-python-tests-coverage-profiling-2jf4
- https://github.com/mongomock/mongomock

> **ERROR**: Ao fazer deploy para produção o comando `pip freeze > requirements.txt` esta trazendo dependências da plataforma windows
> e duranto o processo de build da imagem pelo docker está lançando erro devido a pacotes do windows.
> para contorna esse `bug` foi necessário criar um script python para ignorar pacote com dependência de plataforma.

> **WARNING**:Para rodar os testes deve baixar as dependencias do projeto usando o comando do `pip`  
> dentro da pasta raiz do projeto executar pelo terminal o comando `python py_ignore_requirements.py` assim será instalado as dependências.  
> Não esquecer de ativar o ambiente virtual com o comando `.venv/Scripts/activate` para windows.

Crontab Syntax

```text
*     *     *     *     *
-     -     -     -     -
|     |     |     |     |
|     |     |     |     +----- day of the week (0 - 6) (Sunday=0)
|     |     |     +------- month (1 - 12)
|     |     +--------- day of the month (1 - 31)
|     +----------- hour (0 - 23)
+------------- min (0 - 59)
```
