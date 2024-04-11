from dotenv import load_dotenv,dotenv_values


carregar = load_dotenv()
env = dotenv_values('../../.env')
print(env['db_name'])

