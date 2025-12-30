class HouseholdNotFoundError(Exception):
    pass


class HouseholdNameAlreadyExistError(Exception):
    pass


class HouseholdMapperError(Exception):
    pass


# Member-related exceptions
class OnlyOwnerCanInviteError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class AlreadyActiveMemberError(Exception):
    pass


class AlreadyInvitedError(Exception):
    pass


class InviteNotFoundError(Exception):
    pass


class NotInvitedError(Exception):
    pass


class OnlyOwnerCanRevokeError(Exception):
    pass


class OnlyOwnerCanRemoveMemberError(Exception):
    pass


class CannotRemoveSelfError(Exception):
    pass


class OnlyOwnerCanUpdateError(Exception):
    pass


class OnlyOwnerCanDeleteError(Exception):
    pass
