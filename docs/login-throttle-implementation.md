# Login Throttle Implementation Guide

This document provides implementation options for adding login throttling to the FastAPI application.

## Overview

Login throttling prevents brute-force attacks by limiting the number of login attempts within a specific time window. This can be implemented in several ways depending on your requirements.

## Option 1: Using SlowAPI (Simple & Quick)

Best for: Small to medium applications, quick implementation

### Installation

```bash
pip install slowapi
```

### Implementation

#### 1. Create rate limiter instance

```python
# app/shared/infrastructure/rate_limiter.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
```

#### 2. Update login controller

```python
# app/context/auth/interface/rest/controllers/login_rest_controller.py
from fastapi import APIRouter, Depends
from app.shared.infrastructure.rate_limiter import limiter
from app.context.auth.application.commands import LoginCommand
from app.context.auth.application.contracts import LoginHandlerContract
from app.context.auth.interface.rest.dependencies import get_login_handler
from app.context.auth.interface.rest.schemas import LoginRequest

router = APIRouter(prefix="/login", tags=["login"])

@router.post("")
@limiter.limit("5/minute")  # 5 attempts per minute per IP
async def login(
    request: LoginRequest,
    handler: LoginHandlerContract = Depends(get_login_handler)
):
    """User login endpoint with rate limiting"""
    return await handler.handle(
        LoginCommand(email=request.email, password=request.password)
    )
```

#### 3. Register in main application

```python
# main.py
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.shared.infrastructure.rate_limiter import limiter

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

### Pros
- Quick to implement
- Minimal code changes
- Works out of the box

### Cons
- Throttles by IP only (can't throttle by username/email)
- In-memory only (doesn't work across multiple instances without Redis backend)

---

## Option 2: Redis-Based Throttle Service (Production Ready)

Best for: Production applications, distributed systems, throttling by username/email

### Installation

```bash
pip install redis
```

### Implementation

#### 1. Create throttle service

```python
# app/shared/infrastructure/services/throttle_service.py
from datetime import datetime, timedelta
from typing import Optional
import redis.asyncio as redis


class LoginThrottleService:
    """
    Redis-based login throttle service.

    Tracks login attempts per identifier (email/username or IP) and enforces
    rate limits to prevent brute-force attacks.
    """

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.max_attempts = 5
        self.window_seconds = 300  # 5 minutes
        self.lockout_seconds = 900  # 15 minutes after max attempts

    async def is_throttled(self, identifier: str) -> tuple[bool, Optional[int]]:
        """
        Check if login attempts are throttled for the given identifier.

        Args:
            identifier: Email, username, or IP address to check

        Returns:
            Tuple of (is_throttled, retry_after_seconds)
        """
        key = f"login_throttle:{identifier}"
        attempts = await self.redis.get(key)

        if attempts and int(attempts) >= self.max_attempts:
            ttl = await self.redis.ttl(key)
            return True, ttl

        return False, None

    async def record_attempt(self, identifier: str):
        """
        Record a failed login attempt.

        Args:
            identifier: Email, username, or IP address
        """
        key = f"login_throttle:{identifier}"
        current = await self.redis.get(key)

        if current is None:
            # First attempt - set with normal window
            await self.redis.setex(key, self.window_seconds, 1)
        else:
            # Increment attempts
            await self.redis.incr(key)

            # If we've hit the max, extend the lockout period
            if int(current) + 1 >= self.max_attempts:
                await self.redis.expire(key, self.lockout_seconds)

    async def clear_attempts(self, identifier: str):
        """
        Clear all attempts for an identifier (call after successful login).

        Args:
            identifier: Email, username, or IP address
        """
        key = f"login_throttle:{identifier}"
        await self.redis.delete(key)
```

#### 2. Create Redis connection

```python
# app/shared/infrastructure/redis_client.py
import redis.asyncio as redis
from typing import AsyncGenerator


class RedisClient:
    def __init__(self, url: str = "redis://localhost:6379/0"):
        self.url = url
        self._pool = None

    async def get_pool(self) -> redis.Redis:
        if self._pool is None:
            self._pool = redis.from_url(
                self.url,
                encoding="utf-8",
                decode_responses=True
            )
        return self._pool

    async def close(self):
        if self._pool:
            await self._pool.close()


# Global instance
redis_client = RedisClient()


async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    pool = await redis_client.get_pool()
    yield pool
```

#### 3. Create dependency for throttle check

```python
# app/context/auth/interface/rest/dependencies.py
from fastapi import HTTPException, Request, status, Depends
import redis.asyncio as redis

from app.context.auth.interface.rest.schemas import LoginRequest
from app.shared.infrastructure.services.throttle_service import LoginThrottleService
from app.shared.infrastructure.redis_client import get_redis


async def get_throttle_service(
    redis_conn: redis.Redis = Depends(get_redis)
) -> LoginThrottleService:
    return LoginThrottleService(redis_conn)


async def check_login_throttle(
    request: LoginRequest,
    throttle_service: LoginThrottleService = Depends(get_throttle_service)
):
    """
    Dependency that checks if login attempts are throttled.
    Raises HTTPException if throttled.
    """
    # Throttle by email/username
    is_throttled, retry_after = await throttle_service.is_throttled(request.email)

    if is_throttled:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many login attempts. Try again in {retry_after} seconds.",
            headers={"Retry-After": str(retry_after)}
        )
```

#### 4. Update login controller

```python
# app/context/auth/interface/rest/controllers/login_rest_controller.py
from fastapi import APIRouter, Depends, HTTPException, status

from app.context.auth.application.commands import LoginCommand
from app.context.auth.application.contracts import LoginHandlerContract
from app.context.auth.interface.rest.dependencies import (
    get_login_handler,
    check_login_throttle,
    get_throttle_service
)
from app.context.auth.interface.rest.schemas import LoginRequest
from app.shared.infrastructure.services.throttle_service import LoginThrottleService

router = APIRouter(prefix="/login", tags=["login"])


@router.post("")
async def login(
    request: LoginRequest,
    handler: LoginHandlerContract = Depends(get_login_handler),
    throttle_service: LoginThrottleService = Depends(get_throttle_service),
    _: None = Depends(check_login_throttle)
):
    """User login endpoint with throttling"""
    try:
        result = await handler.handle(
            LoginCommand(email=request.email, password=request.password)
        )

        # Clear throttle on successful login
        await throttle_service.clear_attempts(request.email)

        return result

    except Exception as e:
        # Record failed attempt
        await throttle_service.record_attempt(request.email)
        raise
```

#### 5. Update main.py for Redis lifecycle

```python
# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.shared.infrastructure.redis_client import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await redis_client.get_pool()
    yield
    # Shutdown
    await redis_client.close()


app = FastAPI(lifespan=lifespan)
```

### Pros
- Works across multiple instances
- Can throttle by username/email
- Production-ready
- Configurable limits
- Persistent across restarts

### Cons
- Requires Redis infrastructure
- More complex setup

---

## Option 3: In-Memory Throttle Service (Development)

Best for: Development, single-instance deployments, no external dependencies

### Implementation

```python
# app/shared/infrastructure/services/in_memory_throttle_service.py
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List


class InMemoryThrottleService:
    """
    In-memory login throttle service.

    WARNING: This implementation does not work across multiple instances.
    Use Redis-based implementation for production.
    """

    def __init__(self):
        self.attempts: Dict[str, List[datetime]] = defaultdict(list)
        self.max_attempts = 5
        self.window_minutes = 5

    def is_throttled(self, identifier: str) -> tuple[bool, int]:
        """
        Check if login attempts are throttled.

        Returns:
            Tuple of (is_throttled, retry_after_seconds)
        """
        now = datetime.now()
        cutoff = now - timedelta(minutes=self.window_minutes)

        # Clean old attempts
        self.attempts[identifier] = [
            attempt for attempt in self.attempts[identifier]
            if attempt > cutoff
        ]

        if len(self.attempts[identifier]) >= self.max_attempts:
            oldest = self.attempts[identifier][0]
            retry_after = int(
                (oldest + timedelta(minutes=self.window_minutes) - now).total_seconds()
            )
            return True, max(0, retry_after)

        return False, 0

    def record_attempt(self, identifier: str):
        """Record a failed login attempt."""
        self.attempts[identifier].append(datetime.now())

    def clear_attempts(self, identifier: str):
        """Clear attempts after successful login."""
        self.attempts.pop(identifier, None)


# Global instance
throttle_service = InMemoryThrottleService()


def get_throttle_service() -> InMemoryThrottleService:
    return throttle_service
```

### Usage in controller

```python
# app/context/auth/interface/rest/controllers/login_rest_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.shared.infrastructure.services.in_memory_throttle_service import (
    get_throttle_service,
    InMemoryThrottleService
)

router = APIRouter(prefix="/login", tags=["login"])


@router.post("")
async def login(
    request: LoginRequest,
    handler: LoginHandlerContract = Depends(get_login_handler),
    throttle_service: InMemoryThrottleService = Depends(get_throttle_service)
):
    """User login endpoint with in-memory throttling"""
    # Check throttle
    is_throttled, retry_after = throttle_service.is_throttled(request.email)
    if is_throttled:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many login attempts. Try again in {retry_after} seconds.",
            headers={"Retry-After": str(retry_after)}
        )

    try:
        result = await handler.handle(
            LoginCommand(email=request.email, password=request.password)
        )

        # Clear on success
        throttle_service.clear_attempts(request.email)
        return result

    except Exception as e:
        # Record failed attempt
        throttle_service.record_attempt(request.email)
        raise
```

### Pros
- No external dependencies
- Simple implementation
- Good for development

### Cons
- Doesn't work across multiple instances
- Lost on restart
- Not suitable for production

---

## Configuration Recommendations

### Rate Limit Settings

| Environment | Max Attempts | Window | Lockout |
|-------------|--------------|--------|---------|
| Development | 10 | 5 min | 5 min |
| Staging | 5 | 5 min | 15 min |
| Production | 5 | 5 min | 30 min |

### What to Throttle By

1. **Email/Username** (recommended) - Prevents brute-force on specific accounts
2. **IP Address** - Prevents distributed attacks but can affect shared IPs
3. **Both** - Most secure, implement separate limits for each

Example for dual throttling:

```python
async def check_login_throttle(
    request: Request,
    login_request: LoginRequest,
    throttle_service: LoginThrottleService = Depends(get_throttle_service)
):
    # Check by email
    is_throttled, retry_after = await throttle_service.is_throttled(
        f"email:{login_request.email}"
    )
    if is_throttled:
        raise HTTPException(...)

    # Check by IP
    client_ip = request.client.host
    is_throttled, retry_after = await throttle_service.is_throttled(
        f"ip:{client_ip}"
    )
    if is_throttled:
        raise HTTPException(...)
```

## Security Best Practices

1. **Log throttled attempts** - Monitor for attack patterns
2. **Use HTTPS** - Prevent credential interception
3. **Return generic errors** - Don't reveal if user exists
4. **Consider CAPTCHA** - After X failed attempts
5. **Monitor from infrastructure** - Use WAF/rate limiting at load balancer level
6. **Alert on patterns** - Set up monitoring for unusual login attempt patterns

## Testing

Example test for throttle service:

```python
import pytest
from app.shared.infrastructure.services.throttle_service import LoginThrottleService


@pytest.mark.asyncio
async def test_throttle_after_max_attempts(redis_client):
    service = LoginThrottleService(redis_client)
    identifier = "test@example.com"

    # Make max attempts
    for _ in range(5):
        await service.record_attempt(identifier)

    # Should be throttled
    is_throttled, retry_after = await service.is_throttled(identifier)
    assert is_throttled is True
    assert retry_after > 0


@pytest.mark.asyncio
async def test_clear_attempts_on_success(redis_client):
    service = LoginThrottleService(redis_client)
    identifier = "test@example.com"

    await service.record_attempt(identifier)
    await service.clear_attempts(identifier)

    is_throttled, _ = await service.is_throttled(identifier)
    assert is_throttled is False
```

## Recommendation

For your DDD-based FastAPI application:

**Development**: Start with Option 3 (In-Memory)
**Production**: Use Option 2 (Redis-based)

The Redis implementation fits well with your DDD architecture and provides the robustness needed for production use.
