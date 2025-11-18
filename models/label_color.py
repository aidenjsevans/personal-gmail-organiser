
class LabelColor:
    
    def __init__(
            self,
            text_color: str,
            background_color: str):
        self.text_color = text_color
        self.background_color = background_color

    @classmethod    
    def from_dict(cls, label_color_dict: dict[str]):
        text_color: str = label_color_dict["textColor"]
        background_color: str = label_color_dict["backgroundColor"]

        return cls(
            text_color=text_color,
            background_color=background_color)

    def __str__(self):
        
        values: list[str] = []

        values.append(f"\tText color: {self.text_color}")
        values.append(f"\tText color: {self.text_color}")

        return f"\n".join(values)
    
