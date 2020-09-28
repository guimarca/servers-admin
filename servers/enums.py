import enum


class BaseEnum(enum.Enum):
    @classmethod
    def tuples(cls):
        return tuple((e.name, e.value) for e in cls)

    @classmethod
    def names(cls):
        return [e.name for e in cls]

    @classmethod
    def values(cls):
        return [e.value for e in cls]


class ServerType(BaseEnum):
    SS = "Shared Server"
    PS = "Private Server"
    TS = "Test Server"


class ServerStatus(BaseEnum):
    IN_PROGRESS = "A command is being processed"
    RUNNING = "VM up and running"
    STOPPED = "VM is stopped"
    DELETED = "VM deleted"


class ServerFlavor(BaseEnum):
    C2_4GB = "2c 4GB"
    C4_8GB = "4c 8Gb"
    C4_16GB = "4c 16Gb"
    C8_32Gb = "8c 32Gb"
    C8_64GB = "8c 64Gb"


class ServerStorage(BaseEnum):
    TB10 = "10 Tb"
    TB50 = "50 Tb"
    TB100 = "100 Tb"


class CommandType(BaseEnum):
    CREATE = "create"
    CLONE = "clone"
    MODIFY = "modify"
    STOP = "stop"
    START = "start"
    DELETE = "delete"


class CommandResult(BaseEnum):
    SUCCESS = "Command executed successfully"
    ERROR = "Command finished with an error"
