from models import Constant, Group
from schemas import ConstantSchema
from crud import BaseCrud
from sqlalchemy.orm import Session
import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder


class ConstantCrud(BaseCrud[Constant, ConstantSchema, ConstantSchema]):
    @classmethod
    def get_constants_by_group_code(cls, group_code: str, db: Session):
        try:
            group_code = group_code.upper()
            query = (sa.select(Constant).join(Group, Group.id == Constant.group_id)
                     .filter(sa.func.upper(Group.code) == group_code))
            result = jsonable_encoder(db.execute(query).mappings().all())
            return result

        except Exception as e:
            raise e


CRUDConstant = ConstantCrud(Constant)
