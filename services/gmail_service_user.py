from services.gmail_service import GmailService

from typeguard import typechecked

class GmailServiceUser:

    @typechecked
    def __init__(
            self,
            gmail_service: GmailService) -> None:
        
        self.gmail_service = gmail_service
    
