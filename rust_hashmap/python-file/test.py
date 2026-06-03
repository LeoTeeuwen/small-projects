from rust_hashmap import Hashmap

map = Hashmap()

map.insert("HfKlo", "World1!")
print(map.search("HfKlo"))

map.insert("HemKo", "World2!")
print(map.search("HemKo"))

print(map.search("Hello"))

print(map.print())

print("All done!")