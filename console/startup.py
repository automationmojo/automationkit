
from akit.activation.console import showlog
from akit.interop.landscaping.landscape import startup_landscape

showlog()

print("Preparing Landscape...")

lscape = startup_landscape()

print("Landscape Initialized...")
print("")
print("Use 'lscape' variable to access the global Landscape instance")
