def split_str(input: str, delim: str = "\t") -> list[list[str]]:
    rows = input.strip().split("\n")
    table = [row.split(delim) for row in rows]
    # Transpose: columns become rows and vice versa
    columns = list(map(list, zip(*table)))
    return columns

def read_file(file_path: str) -> bytes:
    with open(file_path, 'rb') as f:
        return f.read()