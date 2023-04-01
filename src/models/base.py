from pydantic import BaseModel
from typing import Optional, List


class AudioFeatures(BaseModel):
    acousticness: Optional[float]
    danceability: Optional[float]
    energy: Optional[float]
    instrumentalness: Optional[float]
    liveness: Optional[float]
    loudness: Optional[float]
    speechiness: Optional[float]
    valence: Optional[float]


class RequestModel(BaseModel):
    genre: str
    min: Optional[AudioFeatures]
    max: Optional[AudioFeatures]


class Image(BaseModel):
    url: str
    height: Optional[int]
    width: Optional[int]


class Artist(BaseModel):
    name: str
    image: Optional[Image]


class Track(BaseModel):
    name: str
    artists: List[Artist]
    preview: Optional[str]


class ResponseModel(BaseModel):
    tracks: Optional[List[Optional[Track]]]
    openia: Optional[str]
