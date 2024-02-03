from dataclasses import dataclass

@dataclass
class RegulatorDeviceModel:
    id: str
    mac_address: str
    name: str
    master_key: str