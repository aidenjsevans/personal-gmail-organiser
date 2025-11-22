from services.gmail_service_user import GmailServiceUser

from models.label import Label

from constants.labels.label_constants import LabelConstants

class LabelService(GmailServiceUser):

    def __init__(
            self, 
            gmail_service,
            label_constants: LabelConstants):
        
        super().__init__(gmail_service)
        self.label_constants = label_constants

    #   TODO consider when the gmail service fails
    def get_all_labels(self) -> list[Label] | None:

        results = self.gmail_service.service.users().labels().list(userId="me").execute()
        label_dicts = results.get("labels",[])

        banned_filter_label_ids: set[str] = self.label_constants.banned_filter_label_ids

        labels: list[dict] = []

        if not label_dicts:
            return None

        #   Account for labels that cannot be added to or removed from filters
        for label_dict in label_dicts:

            if label_dict["id"] in banned_filter_label_ids:
                continue

            label = Label.from_dict(label_dict)
            labels.append(label)
        
        return labels
    
    def get_label_options(self) -> dict:

        labels = self.get_all_labels()
        label_options: dict = {}

        for index, label in enumerate(labels):
            label_options[index + 1] = label
        
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