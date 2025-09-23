import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS", 'True').lower() in ('true', '1', 't'),
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS", 'False').lower() in ('true', '1', 't'),
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_reset_email(recipient_email: str, reset_code: str):
    html_content = f"""
    <html>
        <body>
            <h2>Redefinição de Senha</h2>
            <p>Olá,</p>
            <p>Você solicitou a redefinição da sua senha. Use o código abaixo para criar uma nova senha:</p>
            <h3><strong>{reset_code}</strong></h3>
            <p>Este código expirará em 15 minutos.</p>
            <p>Se você não solicitou isso, por favor ignore este e-mail.</p>
        </body>
    </html>
    """
    
    message = MessageSchema(
        subject="Seu Código de Redefinição de Senha",
        recipients=[recipient_email],
        body=html_content,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)