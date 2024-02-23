#######################
#
# Script para leitura de e-mail em caixa de entrada,
# extrair um conteúdo especifico do corpo do email e escrever em um txt convertido
# utilizado com o Zabbix para monitoramento de alertas
#
# Escrito por:
# Ailton Borges
#

import imaplib
import email
import spacy

# Configurações da caixa de e-mail
email_host = 'imap.gmx.com'
email_port = 993
email_username = 'seuemail@seuservidor.com'
email_password = 'suasenhasegura@123'

# Conectando-se à caixa de e-mail do GMX usando SSL/TLS
imap = imaplib.IMAP4_SSL(email_host, email_port)

# Autenticando-se com as credenciais
imap.login(email_username, email_password)

# Selecionando a caixa de entrada
imap.select('INBOX')

# Buscando pelo último e-mail recebido
status, email_data = imap.search(None, 'ALL')
email_ids = email_data[0].split()
latest_email_id = email_ids[-1]

# Obtendo o conteúdo do último e-mail
status, email_data = imap.fetch(latest_email_id, '(RFC822)')
raw_email = email_data[0][1]

# Parseando o e-mail
msg = email.message_from_bytes(raw_email)

# Carregando o modelo de linguagem em português do spaCy
nlp = spacy.load('pt_core_news_sm')

# Função para extrair o status do corpo do e-mail usando NLP
def extrair_status(corpo):
    doc = nlp(corpo)
    for sent in doc.sents:
        if 'status' in sent.text.lower():
            if 'open' in sent.text.lower():
                return '1'
            elif 'continuing resolution' in sent.text.lower():
                return '2'
            elif 'resolved' in sent.text.lower():
                return '0'
    return 'UNKNOWN'

# Extraindo o corpo do e-mail
if msg.is_multipart():
    for part in msg.walk():
        content_type = part.get_content_type()
        if content_type == 'text/plain':
            email_body = part.get_payload(decode=True).decode('utf-8')
else:
    email_body = msg.get_payload(decode=True).decode('utf-8')

# Salvando o conteúdo do e-mail em um arquivo de texto
with open('email_content.txt', 'w') as file:
    file.write(email_body)

# Extraindo o status do corpo do e-mail usando NLP
status_value = extrair_status(email_body)

# Escrevendo o status no arquivo de texto
with open('status.txt', 'w') as file:
    file.write(status_value)

# Desconectando-se da caixa de e-mail
imap.logout()
