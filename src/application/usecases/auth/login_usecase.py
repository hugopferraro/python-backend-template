from src.application.auth.token_service import TokenService
from src.application.behaviour.handler import Handler
from src.application.behaviour.handler_registry import use_case
from src.application.usecases.auth.login_request import LoginRequest
from src.api.v1.schemas.auth_schemas import Token
from src.domain.exceptions.auth.auth_exception import AuthException
from src.domain.repositories.user_domain_repository import UserDomainRepository
from src.domain.vo.user import Email


@use_case
class LoginUseCase(Handler[LoginRequest, Token]):
    def handle(
        self,
        request: LoginRequest,
        *,
        repository: UserDomainRepository,
        token_service: TokenService,
    ) -> Token:
        user = repository.find_by_email(Email(value=request.email))
        if user is None or not user.hashed_password.verify(request.password):
            raise AuthException.invalid_credentials()

        token = token_service.create_token(
            user_id=user.identifier.value,
            email=user.email.value,
        )
        return Token(access_token=token, token_type="bearer")
