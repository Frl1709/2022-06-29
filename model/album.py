from dataclasses import dataclass

@dataclass
class Album:
    AlbumId: int
    Title: str
    ArtistId: int
    nTrack: int
    Durata: int

    def __hash__(self):
        return hash(self.AlbumId)