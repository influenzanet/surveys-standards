COMMANDS = []

# Register a class as a command provider
def register(klass):
    COMMANDS.append(klass)

# Load module to be able to register (autoloader)
from . import survey

def get_commands():
    return COMMANDS



