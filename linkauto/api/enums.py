import enum


class TimestampType(enum.Enum):
  seconds = 11
  milliseconds = 13
  microseconds = 15
  nanoseconds = 19


class InviteActionType(enum.Enum):
  ACCEPT = 0
  IGNORE = 1
  REJECT = 2
  REPORT_SPAM = 3
  WITHDRAW = 4
  ACTOR_WITHDRAW = 5


class ConnectionInviteType(enum.Enum):
  RECEIVED = 'receivedInvitation'
  SENT = 'invitationType'
