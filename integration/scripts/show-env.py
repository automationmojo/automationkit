import os

print("=================== Current Environment ===================")

env_var_names = [ek for ek in os.environ]
env_var_names.sort()

for ek in env_var_names:
    print ("{}: {}".format(ek, os.environ[ek]))

print("===========================================================")

