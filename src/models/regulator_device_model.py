
from pydantic import BaseModel


class RegulatorDeviceModel(BaseModel):
    id: str
    mac: str
    name: str