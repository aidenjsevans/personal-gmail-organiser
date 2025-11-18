from services.gmail_service_user import GmailServiceUser

from models.label import Label

class LabelService(GmailServiceUser):

    def __init__(self, gmail_service):
        super().__init__(gmail_service)

    def print_all_labels(self) -> None:
    
        results = self.gmail_service.service.users().labels().list(userId="me").execute()
        labels = results.get("labels",[])

        if not labels:
            print("No labels found")
            return

        print("Labels:")
        
        for label_dict in labels:
            label = Label.from_dict(label_dict=label_dict)
            print(f"\n{label.__str__()}")