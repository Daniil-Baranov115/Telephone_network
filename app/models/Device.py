class Device:
    
    def __init__(self, id: int,  phone_number: str, device_type: str, client_id:int):
        self.id = id
        self.phone_number = phone_number
        self.device_type = device_type
        self.client_id = client_id
        
    def get_number(self) -> str:
        pass
        
    