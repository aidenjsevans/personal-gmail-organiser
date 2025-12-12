
class Message:
    
    def __init__(
            self,
            id: str,
            thread_id: str,
            label_ids: list[str] | None,
            snippet: str | None,
            payload: dict | None,
            size_estimate: int | None,
            history_id: str | None,
            internal_date: str | None,
            mime_type: str | None,
            headers: str | None):
        
        self.id: str = id
        self.thread_id: str = thread_id
        self.label_ids: list[str] | None = label_ids
        self.snippet: str | None = snippet
        self.payload: dict | None = payload
        self.size_estimate: int | None = size_estimate
        self.history_id: str | None = history_id
        self.internal_date: str | None = internal_date
        self.mime_type: str | None = mime_type
        self.headers: list[dict] | None = headers
    
    @classmethod
    def from_dict(cls, message_dict: dict):
        keys: list[str] = set(message_dict.keys())

        if "id" in keys:
            id: str = message_dict["id"]
        else:
            raise Exception("The input dictionary must contain an 'id' key")
        
        if "threadId" in keys:
            thread_id: str = message_dict["threadId"]
        else:
            raise Exception("The input dictionary must contain a 'threadId' key")
        
        if "labelIds" in keys:
            label_ids: list[str] | None = message_dict["labelIds"]
        else:
            label_ids: list[str] | None = None
        
        if "snippet" in keys:
            snippet: str | None = message_dict["snippet"]
        else:
            snippet: str | None = None
        
        if "payload" in keys:
            payload: dict | None = message_dict["payload"]
        else:
            payload: dict | None = None
        
        if "sizeEstimate" in keys:
            size_estimate: int | None = message_dict["sizeEstimate"]
        else:
            size_estimate: int | None = None
        
        if "historyId" in keys:
            history_id: str | None = message_dict["historyId"]
        else:
            history_id: str | None = None

        if "internalDate" in keys:
            internal_date: str | None = message_dict["internalDate"]
        else:
            internal_date: str | None = None
        
        payload_keys: list[str] = set(payload.keys())

        if "mimeType" in payload_keys:
            mime_type: str | None = payload["mimeType"]
        else:
            mime_type: str | None = None
        
        if "headers" in payload_keys:
            headers: list[dict] | None = payload["headers"]
        else:
            headers: list[dict] | None = None
        
        return cls(
            id=id,
            thread_id=thread_id,
            label_ids=label_ids,
            snippet=snippet,
            payload=payload,
            size_estimate=size_estimate,
            history_id=history_id,
            internal_date=internal_date,
            mime_type=mime_type,
            headers=headers
            )

    @property
    def sender(self) -> str | None:
        
        for element in self.headers:
            if element["name"] == "From":
                return element["value"]
        
        return None

    def __str__(self) -> str:
        
        values: list[str] = []

        values.append(f"\tID: {self.id}")
        values.append(f"\tThread ID: {self.thread_id}")
        values.append(f"\tLabel IDs: {self.label_ids}")
        values.append(f"\tSender: {self.sender}")
        values.append(f"\tSize estimate: {self.size_estimate}")
        values.append(f"\tHistory ID: {self.history_id}")
        values.append(f"\tInternal date: {self.internal_date}")
        values.append(f"\tMime type: {self.mime_type}")

        return f"\n".join(values)




        