from schemas import DocumentSchema
from crud import BaseCrud
from models.Document import Document


class DocumentCrud(BaseCrud[Document, DocumentSchema, DocumentSchema]):
    pass


CRUDDocument = DocumentCrud(Document)
