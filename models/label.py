
class Label:
    
    def __init__(
            self, 
            id: str,
            name: str,
            message_list_visibility: str | None,
            label_list_visibility: str | None,
            type: str):
        
        self.id = id
        self.name = name
        self.message_list_visibility = message_list_visibility
        self.label_list_visibility = label_list_visibility
        self.type = type
    
    @classmethod
    def from_dict(cls, label_dict: dict) -> Label:
        keys: list[str] = set(label_dict.keys())

        if "id" in keys:
            id: str = label_dict["id"]
        else:
            raise Exception("The input dictionary must contain an 'id' key")

        if "name" in keys:
            name: str = label_dict["name"]
        else:
            raise Exception("The input dictionary must contain a 'name' key")

        if "messageListVisibility" in keys:
            message_list_visibility: str | None = label_dict["messageListVisibility"]
        else:
            message_list_visibility: str | None = None

        if "labelListVisibility" in keys:
            label_list_visibility: str | None = label_dict["labelListVisibility"]
        else:
            label_list_visibility: str | None = None
            
        if "type" in keys:
            type: str = label_dict["type"]
        else:
            raise Exception("The input dictionary must contain a 'type' key")

        return cls(
            id=id,
            name=name,
            message_list_visibility=message_list_visibility,
            label_list_visibility=label_list_visibility,
            type=type
            )

    def __str__(self) -> str:
        
        values: list[str] = []

        values.append(f"\tID: {self.id}")
        values.append(f"\tName: {self.name}")
        values.append(f"\tMessage list visibility: {self.message_list_visibility}")
        values.append(f"\tLabel list visibility: {self.label_list_visibility}")
        values.append(f"\tType: {self.type}")

        return f"\n".join(values)



    