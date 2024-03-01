import base64
import requests
import hashlib
import random
import urllib
import hmac
import time
import json
from datetime import datetime, timedelta
import pandas as pd
from time import sleep
import gspread

# Function to calculate future date for invoice data
def _foward_date():
    """
    Calculates a date 180 days in the future from the current date.
    """
    now = datetime.now() # data e hora atual
    future_date = now + timedelta(days=180) # adiciona 180 dias
    date_time = future_date.strftime("%d/%m/%Y")
    return date_time

# Function to get the current date
def _current_date():
    """
    Gets the current date in the format "%d/%m/%Y".
    """
    now = datetime.now() # current date and time
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    date_time = now.strftime("%d/%m/%Y")
    return date_time

# Function to generate a timestamp
def _generateTimestamp():
    """
    Generates a timestamp as an integer string representing the current time.
    """
    return str(int(time.time()))

# Function to generate a pseudo-random number for nonce
def _generateNonce(length=11):
    """
    Generates a random string of specified length (default 11) for nonce.
    """
    return ''.join([str(random.randint(0, 9)) for i in range(length)])

# Function to generate the signature for the OAuth request
def _generateSignature(method, url, consumerKey, Nonce, currentTime, token, consumerSecret,
                      tokenSecret, offset=None):
    """
    Generates the signature for the OAuth request using HMAC-SHA256.
    """
    signature_method = 'HMAC-SHA256'
    version = '1.0'
    base_url = url
    encoded_url = urllib.parse.quote(base_url, safe='')
    collected_string = '&'.join(['deploy=1', 'oauth_consumer_key=' + consumerKey, 'oauth_nonce=' + Nonce,
                                  'oauth_signature_method=' + signature_method, 'oauth_timestamp=' + currentTime,
                                  'oauth_token=' + token, 'oauth_version=' + version, 'script=411'])
    encoded_string = urllib.parse.quote(collected_string, safe='')
    base = '&'.join([method, encoded_url, encoded_string])
    print('base: ', base)
    key = '&'.join([consumerSecret, tokenSecret])
    digest = hmac.new(key=str.encode(key), msg=str.encode(base), digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest).decode()
    return urllib.parse.quote(signature, safe='')

# Function to create the OAuth header for the API request
def _create_oauth(base_url):
    """
    Creates the OAuth header for the API request.
    """
    nsAccountID = 'your_nsAccountID'  # Replace with your NetSuite account ID
    consumerKey = 'consumerKey'
    consumerSecret = 'your_consumerSecret'  # Replace with your consumer secret
    token = 'your_token'  # Replace with your access token
    tokenSecret = 'your_tokenSecret'  # Replace with your token secret

    Nonce = _generateNonce(length=11)
    currentTime = _generateTimestamp()

    signature = _generateSignature('POST', base_url, consumerKey, Nonce, currentTime, token,
                                                  consumerSecret, tokenSecret)
    oauth = "OAuth realm=\"" + nsAccountID + "\"," \
            "oauth_consumer_key=\"" + consumerKey + "\"," \
            "oauth_token=\"" + token + "\"," \
            "oauth_signature_method=\"HMAC-SHA256\"," \
            "oauth_timestamp=\"" + currentTime + "\"," \
            "oauth_nonce=\"" + Nonce + "\"," \
            "oauth_version=\"1.0\"," \
            "oauth_signature=\"" + signature + "\""
    headers = {
        'Content-Type': "application/json",
        'Authorization': oauth,
    }
    print("headers: ", headers)
    return headers

"""Here is my API call"""

# Define the API URL for invoice data
url = "https://<COMPANY_CODE>.restlets.api.netsuite.com/app/site/hosting/restlet.nl?script=411&deploy=1"
base_url = "https://<COMPANY CODE>.restlets.api.netsuite.com/app/site/hosting/restlet.nl"
# Define the payload with start and end dates for the query
payload = json.dumps({"dataInicio": "01/01/2021", "dataFim": _foward_date()})
data = {}
# Perform the POST request to fetch data
response = requests.request("POST", url, headers=_create_oauth(base_url), data=payload)
# Parsing the response from JSON to python dict.
response_faturamento = json.loads(response.text)

dataframe_faturamento = pd.DataFrame(columns=['INTERNALID','N_FATURA','CLIENTE_ID_INTERNO','CLIENTE_NOME','DATA CRIAÇÃO','NFS-E','DATA EMISSÃO',
                                              'STATUS NOTA','CLASSE','VLR. BRUTO','DATA VENCIMENTO','STATUS','DATA PAGAMENTO','OBSERVAÇÃO','VLR. LIQUIDO',
                                              'VLR. RECEBIDO','VALOR RESTANTE','EMPRESA''CNPJ CLIENTE','Localidade','ID DO NEGOCIO','CONTA ATIVO'])
# Creating a DataFrame for invoice data with predefined columns
for i in range(len(response_faturamento['Results'])):
    # Extracting each item's data
    currentItem_INTERNALID = response_faturamento['Results'][i]['INTERNALID']
    currentItem_N_FATURA = response_faturamento['Results'][i]['Nº FATURA']
    currentItem_CLIENTE_ID_INTERNO = response_faturamento['Results'][i]['CLIENTE']['ID INTERNO']
    currentItem_CLIENTE_NOME = response_faturamento['Results'][i]['CLIENTE']['NOME']
    currentItem_DATA_CRIACAO = response_faturamento['Results'][i]['DATA CRIAÇÃO']
    currentItem_NFS_E = response_faturamento['Results'][i]['NFS-E']
    currentItem_DATA_EMISSÃO = response_faturamento['Results'][i]['DATA EMISSÃO']
    currentItem_STATUS_NOTA = response_faturamento['Results'][i]['STATUS NOTA']
    currentItem_CLASSE = response_faturamento['Results'][i]['CLASSE']
    currentItem_VLR_BRUTO = response_faturamento['Results'][i]['VLR. BRUTO']
    currentItem_DATA_VENCIMENTO = response_faturamento['Results'][i]['DATA VENCIMENTO']
    currentItem_STATUS = response_faturamento['Results'][i]['STATUS']
    currentItem_DATA_PAGAMENTO = response_faturamento['Results'][i]['DATA PAGAMENTO']
    currentItem_OBSERVACAO = response_faturamento['Results'][i]['OBSERVAÇÃO']
    currentItem_VLR_LIQUIDO = response_faturamento['Results'][i]['VLR. LIQUIDO']
    currentItem_VLR_RECEBIDO = response_faturamento['Results'][i]['VLR. RECEBIDO']
    currentItem_VLR_RESTANTE = response_faturamento['Results'][i]['VALOR RESTANTE']
    currentItem_EMPRESA = response_faturamento['Results'][i]['EMPRESA']
    currentItem_CNPJ_CLIENTE = response_faturamento['Results'][i]['CNPJ CLIENTE']
    currentItem_Localidade = response_faturamento['Results'][i]['Localidade']
    currentItem_ID_DO_NEGOCIO = response_faturamento['Results'][i]['ID DO NEGOCIO']
    currentItem_CONTA_ATIVO = response_faturamento['Results'][i]['CONTA ATIVO']

    # Adding the item's data to the DataFrame
    dataframe_faturamento.loc[i] = [currentItem_INTERNALID,
                                    currentItem_N_FATURA,
                                    currentItem_CLIENTE_ID_INTERNO,
                                    currentItem_CLIENTE_NOME,
                                    currentItem_DATA_CRIACAO,
                                    currentItem_NFS_E,
                                    currentItem_DATA_EMISSÃO,
                                    currentItem_STATUS_NOTA,
                                    currentItem_CLASSE,
                                    currentItem_VLR_BRUTO,
                                    currentItem_DATA_VENCIMENTO,
                                    currentItem_STATUS,
                                    currentItem_DATA_PAGAMENTO,
                                    currentItem_OBSERVACAO,
                                    currentItem_VLR_LIQUIDO,
                                    currentItem_VLR_RECEBIDO,
                                    currentItem_VLR_RESTANTE,
                                    currentItem_EMPRESA,
                                    currentItem_CNPJ_CLIENTE,
                                    currentItem_Localidade,
                                    currentItem_ID_DO_NEGOCIO,
                                    currentItem_CONTA_ATIVO]

# Casting numerical columns to float type
dataframe_faturamento['VLR. BRUTO'] = dataframe_faturamento['VLR. BRUTO'].astype('float')
dataframe_faturamento['VLR. LIQUIDO'] = dataframe_faturamento['VLR. LIQUIDO'].astype('float')
dataframe_faturamento['VLR. RECEBIDO'] = dataframe_faturamento['VLR. RECEBIDO'].astype('float')

"""Here is my API call"""
# Define the API URL for expenses data
url = "https://<COMPANY_CODE>.restlets.api.netsuite.com/app/site/hosting/restlet.nl?script=425&deploy=1"
base_url = "https://<COMPANY_CODE>.restlets.api.netsuite.com/app/site/hosting/restlet.nl"
# Define the payload with start and end dates for the query
payload = json.dumps({"dataInicio": "31/12/2022", "dataFim": _current_date()})
data = {}
# Making the POST request to fetch expenses data
response = requests.request("POST", url, headers=_create_oauth(base_url), data=payload)
# Parsing the response from JSON to Python dict
response_despesas = json.loads(response.text)

# Creating a DataFrame for expenses data with predefined columns
dataframe_despesas = pd.DataFrame(columns=['ID Interno', 'Data emissão', 'Data de Vencimento', 'Subsidiária', 'Tipo', 'Fornecedor', 'Valor líquido', 'Número da Transação', 'Classe',
                                          'Departamento', 'Localidade', 'Conta', 'Status', 'Número NFSe', 'Memo', 'Contabilização', 'Valor parcela', 'Valor pago', 'Valor Restante',
                                          'Formulário personalizado', 'CAC'])

# Data processing for expenses
for i in range(len(response_despesas['Results'])):
    # Extracting each item's data from the response
    currentItem_ID_Interno = response_despesas['Results'][i]['ID Interno']
    currentItem_Data_emissao = response_despesas['Results'][i]['Data emissão']
    currentItem_Data_de_Vencimento = response_despesas['Results'][i]['Data de Vencimento']
    currentItem_Subsidiaria = response_despesas['Results'][i]['Subsidiária']
    currentItem_Tipo = response_despesas['Results'][i]['Tipo']
    currentItem_Fornecedor = response_despesas['Results'][i]['Fornecedor']
    currentItem_Valor_liquido = response_despesas['Results'][i]['Valor líquido']
    currentItem_Numero_da_Transacao = response_despesas['Results'][i]['Número da Transação']
    currentItem_Classe = response_despesas['Results'][i]['Classe']
    currentItem_Departamento = response_despesas['Results'][i]['Departamento']
    currentItem_Localidade = response_despesas['Results'][i]['Localidade']
    currentItem_Conta = response_despesas['Results'][i]['Conta']
    currentItem_Status = response_despesas['Results'][i]['Status']
    currentItem_Numero_NFSe = response_despesas['Results'][i]['Número NFSe']
    currentItem_Memo = response_despesas['Results'][i]['Memo']
    currentItem_Contabilizacao = response_despesas['Results'][i]['Contabilização']
    #currentItem_Periodo = response_despesas['Results'][i]['Período']
    currentItem_Valor_parcela = response_despesas['Results'][i]['Valor parcela']
    currentItem_Valor_pago = response_despesas['Results'][i]['Valor pago']
    currentItem_Valor_restante = response_despesas['Results'][i]['Valor Restante']
    currentItem_Formulario_personalizado = response_despesas['Results'][i]['Formulário personalizado']
    currentItem_CAC = response_despesas['Results'][i]['CAC']

    # Adding the item's data to the DataFrame
    dataframe_despesas.loc[i] = [currentItem_ID_Interno, currentItem_Data_emissao, currentItem_Data_de_Vencimento, currentItem_Subsidiaria, currentItem_Tipo, currentItem_Fornecedor,
                                currentItem_Valor_liquido, currentItem_Numero_da_Transacao, currentItem_Classe, currentItem_Departamento, currentItem_Localidade, currentItem_Conta,
                                currentItem_Status, currentItem_Numero_NFSe, currentItem_Memo, currentItem_Contabilizacao, currentItem_Valor_parcela, currentItem_Valor_pago,
                                currentItem_Valor_restante, currentItem_Formulario_personalizado, currentItem_CAC]

# Preparing to write the DataFrame to Google Sheets
# Google Sheets document ID where the data will be added
CODE = 'CODE'

# Credentials for accessing Google Sheets
credenciais = {
              "type": "service_account",
              "project_id": "project_id",
              "private_key_id": "private_key_id",
              "private_key": "private_key",
              "client_email": "client_email",
              "client_id": "client_id",
              "auth_uri": "https://accounts.google.com/o/oauth2/auth",
              "token_uri": "https://oauth2.googleapis.com/token",
              "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
              "client_x509_cert_url": "client_x509_cert_url"
              }

# Client to access Sheets with our access key
gc = gspread.service_account_from_dict(credenciais) #a key está sendo acessada de um diretório local.

# Sheet where we want to add the data
sh = gc.open_by_key(CODE)

# Choosing a specific sheet to add our data
ws_receita = sh.worksheet('receita')
ws_despesas = sh.worksheet('despesas')

# Adding data from the pandas DataFrame to the Faturamento (revenue) sheet
ws_receita.update([dataframe_faturamento.columns.values.tolist()] + dataframe_faturamento.values.tolist())
# Adding data from the pandas DataFrame to the Despesas (expenses) sheet
ws_despesas.update([dataframe_despesas.columns.values.tolist()] + dataframe_despesas.values.tolist())

