from crud import CRUDGroup, CRUDConstant
from schemas import GroupSchema, ConstantSchema
from db import get_db
import constants as cs
from typing import List
from models import Group

group_code_list = [
    cs.MSG_SEEN_STATUS_GRP_CODE
]

constant_dict = {
    cs.MSG_SEEN_STATUS_GRP_CODE: [cs.MSG_SEEN_STATUS, cs.MSG_PENDING_STATUS, cs.MSG_SENT_STATUS]
}


def insert_group_code():
    try:
        db = get_db().__next__()
        group_list_result: List[Group] = CRUDGroup.get_all(db=db, limit=100000)
        grp_list = [i.code for i in group_list_result]

        db.commit()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    insert_group_code()
