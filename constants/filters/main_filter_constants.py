from constants.filters.filter_constants import FilterConstants

class MainFilterConstants(FilterConstants):

    def __init__(self):
        
        self.__filter_criteria_options = set([
            "from",
            "to",
            #"subject",
            #"query",
            #"negatedQuery",
            #"hasAttachment",
            #"size",
            #"sizeComparison"
        ])

        self.__filter_action_options = set([
            "addLabelIds",
            "removeLabelIds",
            #"forward",
            #"markRead",
            #"archive",
            #"trash"
        ])

    @property
    def filter_criteria_options(self) -> set[str]:
        return self.__filter_criteria_options
    
    @property
    def filter_action_options(self) -> set[str]:
        return self.__filter_action_options