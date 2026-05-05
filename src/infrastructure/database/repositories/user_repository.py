from sqlalchemy import select, or_

from src.application.usecases.user.user_read_dto import UserReadDTO
from src.domain.entities.user.user_domain_entity import UserDomainEntity
from src.domain.repositories.user_domain_repository import UserDomainRepository
from src.domain.vo.user import UserID, PersonalInfo, Email, HashedPassword
from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.database.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository, UserDomainRepository):

    def find_by_identifier(self, identifier: UserID) -> UserReadDTO | None:
        model = self.db.query(UserModel).filter_by(id=identifier.value).first()
        return self._to_read_dto(model) if model else None

    def find_by_email(self, email: Email) -> UserDomainEntity | None:
        model = self.db.query(UserModel).filter_by(email=email.value).first()
        return self._to_entity(model) if model else None

    def list(self, search: str | None = None) -> list[UserReadDTO]:
        statement = select(UserModel)
        if search:
            pattern = f"%{search}%"
            statement = statement.where(
                or_(
                    UserModel.email.ilike(pattern),
                    UserModel.first_name.ilike(pattern),
                    UserModel.last_name.ilike(pattern),
                )
            )
        return [self._to_read_dto(m) for m in self.db.scalars(statement).all()]

    def save(self, user: UserDomainEntity) -> None:
        existing = self.db.query(UserModel).filter_by(id=user.identifier.value).first()
        if existing:
            existing.first_name = user.personal_info.first_name
            existing.last_name = user.personal_info.last_name
            existing.email = user.email.value
            existing.password = user.hashed_password.value
            self.db.flush()
        else:
            self.db.add(self._to_model(user))
            self.db.flush()

    def delete(self, identifier: UserID) -> UserDomainEntity | None:
        model = self.db.query(UserModel).filter_by(id=identifier.value).first()
        if not model:
            return None
        entity = self._to_entity(model)
        self.db.delete(model)
        self.db.flush()
        return entity

    def _to_read_dto(self, model: UserModel) -> UserReadDTO:
        return UserReadDTO(
            identifier=UserID(value=model.id),
            personal_info=PersonalInfo(
                first_name=model.first_name,
                last_name=model.last_name,
            ),
            email=Email(value=model.email),
            hashed_password=HashedPassword(value=model.password),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_entity(self, model: UserModel) -> UserDomainEntity:
        return UserDomainEntity(
            identifier=UserID(value=model.id),
            personal_info=PersonalInfo(
                first_name=model.first_name,
                last_name=model.last_name,
            ),
            email=Email(value=model.email),
            hashed_password=HashedPassword(value=model.password),
        )

    def _to_model(self, entity: UserDomainEntity) -> UserModel:
        return UserModel(
            id=entity.identifier.value,
            first_name=entity.personal_info.first_name,
            last_name=entity.personal_info.last_name,
            email=entity.email.value,
            password=entity.hashed_password.value,
        )
