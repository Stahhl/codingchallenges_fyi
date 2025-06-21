def split_str(input: str, delim: str = "\t") -> list[list[str]]:
    rows = input.strip().split("\n")
    table = [row.split(delim) for row in rows]
    # Transpose: columns become rows and vice versa
    columns = list(map(list, zip(*table)))
    return columns

def parse_fields(field: str) -> tuple[int, int]:
    if len(field) > 3:
        print(f"Invalid field argument {field}. Allowed: n or x,n or \"x n\"")
        exit(1)
    if "," in field:
        split = field.split(",")
        return int(split[0])-1,int(split[1])
    elif " " in field:
        split = field.split(" ")
        return int(split[0])-1,int(split[1])
    return int(field)-1,int(field)

def read_file(file_path: str) -> bytes:
    with open(file_path, 'rb') as f:
        return f.read()