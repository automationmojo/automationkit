
import enum

class ResourceLifespan(str, enum.Enum):
    Session = "session"
    Package = "package"
    Test = "test"
