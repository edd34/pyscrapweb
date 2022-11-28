import orm_sqlite
from dataclasses import dataclass


class Pattern(orm_sqlite.Model):
    id = orm_sqlite.IntegerField(primary_key=True)  # auto-increment
    url = orm_sqlite.IntegerField()
    timestamp = orm_sqlite.StringField()
    entity_type = orm_sqlite.StringField()
    entity_name = orm_sqlite.StringField()
    entity_count = orm_sqlite.StringField()


class PatternSchema:
    def __init__(
        self,
        url: str,
        timestamp: str,
        entity_type: str,
        entity_name: str,
        entity_count: int,
    ):
        self.url = url
        self.timestamp = timestamp
        self.entity_type = entity_type
        self.entity_name = entity_name
        self.entity_count = entity_count

    def validate(self):
        pass

    def repr(self):

        return {
            "id": self.id,
            "url": self.url,
            "timestamp": self.timestamp,
            "entity_page": self.entity_type,
            "entity_name": self.entity_name,
            "entity_count": self.entity_count,
        }
