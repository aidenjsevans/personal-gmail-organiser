from services.gmail_service_user import GmailServiceUser

from models.label import Label

class LabelService(GmailServiceUser):

    def __init__(self, gmail_service):
        super().__init__(gmail_service)

    #   TODO consider when the gmail service fails
    def get_all_labels(self) -> list[Label]:

        results = self.gmail_service.service.users().labels().list(userId="me").execute()
        label_dicts = results.get("labels",[])

        labels: list[dict] = []

        for label_dict in label_dicts:

            label = Label.from_dict(label_dict)

            labels.append(label)
        
        return labels

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