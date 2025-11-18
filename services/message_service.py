from services.gmail_service_user import GmailServiceUser

from models.message import Message

class MessageService(GmailServiceUser):

    def __init__(self, gmail_service):
        super().__init__(gmail_service)
    
    def print_messages(self, max_results: int) -> None:

        results = self.gmail_service.service.users().messages().list(userId="me", maxResults=max_results).execute()
        messages = results.get("messages",[])

        if not messages:
            print("No messages found")
            return

        print("Messages:")
        
        for message_dict in messages:
            
            message_detail_dict = self.gmail_service.service.users().messages().get(
                userId='me', 
                id=message_dict['id'], 
                format='metadata',
                metadataHeaders=['Subject', 'Date', 'From']
                ).execute()
            
            message = Message.from_dict(message_dict=message_detail_dict)

            print(f"\n{message.__str__()}")
    
