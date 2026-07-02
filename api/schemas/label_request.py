from pydantic import BaseModel


class LabelRequestData(BaseModel):
    lpn: str


class LabelRequest(BaseModel):
    request: LabelRequestData
