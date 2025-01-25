from typing import TypeVar, Generic, Type, Optional

from sqlmodel import SQLModel, select
from sqlmodel.orm.session import Session

from structlog import get_logger

logger = get_logger("cgn-ec.crud")

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        """CRUD Object with default methods to Create, Read, Update and Delete (CRUD).
        Args:
            model:  SQLModel
        """
        self.model = model

    async def get(self, db: Session, id: int) -> Optional[ModelType]:
        """Get a single object from the database and load into the ModelType

        Args:
            db:             SQLModel Session
            id:             Database ID
        """
        result = await db.exec(select(self.model).where(self.model.id == id))
        return result.one_or_none()

    async def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        """Create an object in the database

        Args:
            db:             SQLModel Session
            obj_in:         SQLModel Object to Create in Database
        """
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
