import asyncio

from app.context.auth.domain.contracts import (
    LoginAttemptsServiceContract,
    SessionRepositoryContract,
)
from app.context.auth.domain.value_objects import FailedLoginAttempts, ThrottleTime
from app.context.user.domain.value_objects import Email


class LoginAttemptsService(LoginAttemptsServiceContract):
    _sessionRepository: SessionRepositoryContract

    def __init__(self, sessionRepo: SessionRepositoryContract):
        self._sessionRepository = sessionRepo
        pass

    async def handle(self, email: Email):
        attempts = await self._sessionRepository.getLoginAttepmts(email)

        if attempts.hasReachMaxAttempts():
            # User has reached max attempts - timeout handling will be done later
            print("User blocked - max attempts reached")
            # TODO: Handle timeout logic
            pass
        else:
            # User has remaining attempts
            # Store failed attempt by incrementing the count
            new_attempts = FailedLoginAttempts(value=attempts.value + 1)
            await self._sessionRepository.updateAttempts(email, new_attempts)

            # Calculate throttle time and delay the response
            throttle_time = ThrottleTime.fromAttempts(new_attempts)
            print(
                f"Failed attempt {new_attempts.value}. Delaying response by {throttle_time.value}s"
            )

            # Sleep to delay the response (throttle)
            await asyncio.sleep(throttle_time.value)
