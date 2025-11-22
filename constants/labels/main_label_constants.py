from constants.labels.label_constants import LabelConstants

class MainLabelConstants(LabelConstants):

    def __init__(self):
        
        self.__banned_filter_label_ids = set([
            
            "SPAM",
            "TRASH",
            
            "CATEGORY_PERSONAL",
            "CATEGORY_SOCIAL",
            "CATEGORY_PROMOTIONS",
            "CATEGORY_UPDATES",
            "CATEGORY_FORUMS",
            
            "ALL",
            "CHAT",
            "DRAFT",
            "SENT",
            "SCHEDULED",
            "OUTBOX"
        ])
    
    @property
    def banned_filter_label_ids(self) -> set[str]:
        return self.__banned_filter_label_ids