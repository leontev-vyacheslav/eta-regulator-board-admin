from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class RegulatorDeviceModel:
    id: str
    mac_address: str
    name: str
    master_key: str
    creation_date: datetime