from pydantic import BaseModel, Field, model_validator
from typing import Optional

class GetUserHandleInfoParams(BaseModel):
    user_handle: str = Field(..., description="Twitter handle (do not include '@', e.g., elonmusk)")

class GetUserIDInfoParams(BaseModel):
    user_id: str = Field(..., description="Twitter user ID")

class GetUserTweetsParams(BaseModel):
    user_id: Optional[str] = Field(None, description="Twitter user ID")
    link: Optional[str] = Field(None, description="Twitter profile link (e.g., https://x.com/elonmusk)")

    @model_validator(mode="after")
    def check_user_id_or_link(self) -> "GetUserTweetsParams":
        if not self.user_id and not self.link:
            raise ValueError("At least one of 'user_id' or 'link' must be provided.")
        return self

class GetTwitterCheckFollowParams(BaseModel):
    project_handle: Optional[str] = Field(None, description="Twitter handle of the project (e.g., 'elonmusk')")
    project_id: Optional[str] = Field(None, description="Twitter user ID of the project")
    user_handle: Optional[str] = Field(None, description="Twitter handle of the user (e.g., 'SidWoong')")
    user_id: Optional[str] = Field(None, description="Twitter user ID of the user")

    @model_validator(mode="after")
    def check_handles_or_ids(self) -> "GetTwitterCheckFollowParams":
        if not (self.project_handle or self.project_id):
            raise ValueError("At least one of 'project_handle' or 'project_id' must be provided.")
        if not (self.user_handle or self.user_id):
            raise ValueError("At least one of 'user_handle' or 'user_id' must be provided.")
        return self

class GetUserInfoResponse(BaseModel):
    id: str = Field(..., description="Twitter ID")
    name: str
    screen_name: str
    description: str
    followers_count: int
    friends_count: int
    register_date: str
    tweets_count: int
    banner: str
    verified: bool
    avatar: str
    can_dm: bool

class RetweetedStatus(BaseModel):
    created_at: str
    id_str: str
    full_text: str
    user: GetUserInfoResponse
    retweet_count: int
    favorite_count: int
    quote_count: int

class GetTweetsResponse(BaseModel):
    created_at: str
    id_str: str
    full_text: str
    user: GetUserInfoResponse
    retweeted_status: RetweetedStatus

class GetTwitterCheckFollowResponse(BaseModel):
    follow: bool
    user_protected: bool


