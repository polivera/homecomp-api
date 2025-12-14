from app.context.auth.interface.rest.schemas import LoginRequest


async def loginAction(request: LoginRequest):
    return {"leemail": request.email, "lepass": request.password}
