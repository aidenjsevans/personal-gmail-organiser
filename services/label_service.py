from services.gmail_service_user import GmailServiceUser

from models.label import Label

class LabelService(GmailServiceUser):

    def __init__(self, gmail_service):
        super().__init__(gmail_service)

    #   TODO consider when the gmail service fails
    def get_all_labels(self) -> list[Label] | None:

        results = self.gmail_service.service.users().labels().list(userId="me").execute()
        label_dicts = results.get("labels",[])

        labels: list[dict] = []

        if not labels:

            return None

        for label_dict in label_dicts:
            label = Label.from_dict(label_dict)
            labels.append(label)
        
        return labels
    
    def get_label_options(self):

        labels = self.get_all_labels()
        label_options: dict = {}

        for index, label in enumerate(labels):
            label_options[index + 1] = label.name
        
        label_options[len(labels) + 1] = "exit"

        return label_options

    def print_all_labels(self) -> None:
    
        labels: list[Label] = self.get_all_labels()

        if not labels:
            print("\nNo labels found")
            return

        print("\nLabels:")
        
        for label in labels:
            print(f"\n{label.__str__}")