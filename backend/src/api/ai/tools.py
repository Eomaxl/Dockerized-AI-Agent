from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from api.myemailer.sender import send_mail
from api.myemailer.inbox_reader import read_inbox
from api.ai.services import generate_email_message

@tool
def send_me_email(subject:str, content:str) -> str:
    try:
        send_mail(subject=subject, content=content)
    except:
        return "Not Sent"
    return "Sent email"

@tool
def research_email(query:str, config:RunnableConfig):
    metadata = config.get('metadata')
    add_field = metadata.get("additional_field")
    print('add_field', add_field)
    response = generate_email_message(query)
    msg = f"Subject {response.subject}:\nBody: {response.content}"
    return msg

@tool
def get_unread_emails(hours_ago:int=48) -> str:
    try:
        emails = read_inbox(hours_ago=hours_ago, verbose=False)
    except:
        return "Error getting latest emails"
    cleaned = []
    for email in emails:
        data = email.copy()
        if "html_body" in data:
            data.pop('html_body')
        msg = ""
        for k, v in data.items():
            msg += f"{k}:\t{v}"
        cleaned.append(msg)
    return "\n-----\n".join(cleaned)[:500]  
