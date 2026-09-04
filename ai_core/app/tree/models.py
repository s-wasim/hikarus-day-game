from pydantic import BaseModel, Field, RootModel

from app.schemas.journal import AIDeltaName, HikaruDeltaName


class TreeChoice(BaseModel):
    text: str
    ai_delta_favored: AIDeltaName
    hikaru_delta_favored: HikaruDeltaName


class TreeNode(BaseModel):
    ai: str
    user: list[TreeChoice] = Field(default_factory=list, max_length=4)


ConversationTree = RootModel[dict[str, TreeNode]]
