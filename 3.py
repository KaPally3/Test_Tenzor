import json
import random
import sys


def parse_version(version):
    return list(map(int, version.split(".")))


def generate_versions(num):
    random.seed()
    generated = set()
    while len(generated) < 2:
        parts = []
        for i in num.split("."):
            if i == "*":
                parts.append(str(random.randint(0, 10)))
            else:
                parts.append(i)
        ver = ".".join(parts)
        generated.add(ver)
    return list(generated)


version = sys.argv[1]
file = sys.argv[2]

with open(file, "r") as f:
    config = json.load(f)

all_versions = []

for name, num in config.items():
    versions = generate_versions(num)
    all_versions.extend(versions)
all_versions = sorted(set(all_versions), key=parse_version)

print("Отсортированный список всех номеров")
for i in all_versions:
    print(i)

main_version = parse_version(version)
oldV = [i for i in all_versions if parse_version(i) < main_version]
print(f"\nСписок номеров меньше(старее) версии {version}:")
for i in oldV:
    print(i)
