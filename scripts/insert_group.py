from crud import CRUDGroup, CRUDConstant
from schemas import GroupSchema, ConstantSchema
from db import get_db
import constants as cs

group_code_list = [
    cs.MSG_SEEN_STATUS_GRP_CODE
]

constant_dict = {
    cs.MSG_SEEN_STATUS_GRP_CODE: [cs.MSG_SEEN_STATUS, cs.MSG_PENDING_STATUS, cs.MSG_SENT_STATUS]
}


def insert_group_code():
    try:
        db = get_db().__next__()
        for code in group_code_list:
            grp_obj = CRUDGroup.get_by_group_by_code(db=db, code=code)
            if grp_obj is not None and len(grp_obj) > 0:
                grp_id = grp_obj[0]['id']
            else:
                grp_request_obj = GroupSchema(code=code)
                grp_obj = CRUDGroup.create(db=db, obj_in=grp_request_obj)
                db.flush()
                grp_id = grp_obj.id

            enum_class = constant_dict.get(code)
            if enum_class is not None:
                for cons in enum_class:
                    constant_request_obj = ConstantSchema(group_id=grp_id, code=cons)
                    CRUDConstant.create(db=db, obj_in=constant_request_obj)
        db.commit()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    insert_group_code()
