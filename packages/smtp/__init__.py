import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from packages.database import *

load_dotenv()

def welcomeEmail(username:str, email):
    with smtplib.SMTP_SSL(os.getenv("SMTP_SERVER"), os.getenv("PORT")) as server:
        server.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))

        msg = MIMEMultipart()
        msg['From'] = os.getenv("EMAIL")
        msg['To'] = email
        msg['Subject'] = "Cadastro conluido"

        email_body = f"""
        Olá {username},

        Seja bem-vindo ao Cinesertão! Estamos muito felizes por você se juntar a nós. Aqui, você terá acesso a uma vasta seleção de filmes de diferentes gêneros e épocas.
        Explore nosso catálogo e aproveite para relaxar e se divertir com os melhores filmes do cinema. Se precisar de ajuda ou tiver alguma dúvida, não hesite em nos contatar.
        Desejamos a você uma excelente experiência cinematográfica!

        Atenciosamente,
        Cine Sertão
        """
        msg.attach(MIMEText(email_body, 'plain'))

        server.sendmail(os.getenv("EMAIL"), email, msg.as_string())

def newsLetter(msg_body: str, titulo: str):
    subject = titulo

    with smtplib.SMTP_SSL(os.getenv("SMTP_SERVER"), os.getenv("PORT")) as server:
        server.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))

        emailCliente = ReadDoc("users")

        for pk, columns, values in emailCliente:
            username, email, _, _, _ = values

            msg = MIMEMultipart()
            msg['From'] = os.getenv("EMAIL")
            msg['To'] = email
            msg['Subject'] = subject

            email_body = f"""
            Olá {username},

            Confira abaixo a nossa newsLetter

            {msg_body}

            Obrigado,
            Cine Sertão
            """
            msg.attach(MIMEText(email_body, 'plain'))

            server.sendmail(os.getenv("EMAIL"), email, msg.as_string())


def send_proof_tickets(msg_body:str, titulo:str, email:str):
    with smtplib.SMTP_SSL(os.getenv("SMTP_SERVER"), os.getenv("PORT")) as server:
        server.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
        msg = MIMEMultipart()
        msg['From'] = os.getenv("EMAIL")
        msg['To'] = email
        msg['Subject'] = titulo

        email_body = msg_body

        msg.attach(MIMEText(email_body, 'html'))

        server.sendmail(os.getenv("EMAIL"), email, msg.as_string())

def send_password_email(user_data):
    username, email, password_user, _, _ = user_data

    # Configurações do servidor SMTP
    smtp_server = os.getenv("SMTP_SERVER")
    port = os.getenv("PORT")
    sender_email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    # Configurando a conexão SMTP
    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(sender_email, password)

        # Criando mensagem de e-mail
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = "Recuperação de senha - Cinesertão"

        # Corpo do e-mail
        email_body = f"""
        Olá {username},

        Recebemos uma solicitação de recuperação de senha para sua conta no Cinesertão. Se você não solicitou isso, ignore este e-mail.

        Sua senha: {password_user}

        Se precisar de ajuda ou tiver alguma dúvida, não hesite em nos contatar.

        Atenciosamente,
        Equipe do Cinesertão
        """
        msg.attach(MIMEText(email_body, 'plain'))

        # Enviando e-mail
        server.sendmail(sender_email, email, msg.as_string())