from models import Group
from schemas import GroupSchema
from crud import BaseCrud
from sqlalchemy.orm import Session
import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder


class GroupCrud(BaseCrud[Group, GroupSchema, GroupSchema]):
    @classmethod
    def get_by_group_by_code(cls, db: Session, code: str) -> Group | None:
        query = (sa.select(Group).filter(sa.func.upper(Group.code) == code.upper()))
        result = jsonable_encoder(db.execute(query).mappings().all())
        return result


CRUDGroup = GroupCrud(Group)
