from dataclasses import dataclass

@dataclass
class RegulatorDeviceModel:
    id: str
    mac: str
    name: str
    master_key: str