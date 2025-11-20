from constants.filters.filter_constants import FilterConstants

class FilterHelper:

    @staticmethod
    def get_filter_options(
        filter_constants: FilterConstants,
        attribute_name: str,
        option_name: str,
        default = None) -> dict:

        options_list: list | None = getattr(filter_constants, attribute_name, default)

        if options_list == None:
            raise Exception(f"The attribute {attribute_name} does not exist within the FilterConstants object")
        
        options: dict = {}

        for index, option in enumerate(options_list):
            options[index + 1] = option
        
        options[len(options_list) + 1] = "exit"

        print(f"\n{option_name} options: \n")

        for index, option in options.items():
            print(f"\t{index}. {option}")

        return options