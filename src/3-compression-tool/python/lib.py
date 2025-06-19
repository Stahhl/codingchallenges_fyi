import heapq, math

def char_frequencies(s: str) -> dict[str, int]:
    result = {}
    for char in s:
        result[char] = result.get(char, 0) + 1
    return result

class HuffmanNode:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # used by heapq for comparison
    def __lt__(self, other) -> bool:
        return self.freq < other.freq

def build_huffman_tree(freq_dict: dict[str, int]) -> HuffmanNode:
    # Step 1: Create a heap from the frequency dictionary
    heap = [HuffmanNode(char, freq) for char, freq in freq_dict.items()]
    heapq.heapify(heap)

    # Step 2: Build the tree
    while len(heap) > 1:
        # Pop two nodes with the lowest frequencies
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)

        # Create a new internal node with combined frequency
        merged = HuffmanNode(freq=node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2

        # Push the new node back into the heap
        heapq.heappush(heap, merged)

    # The final node is the root of the Huffman tree
    return heap[0]

def build_code_table(node, prefix="", codebook=None) -> dict[str, str]:
    if codebook is None:
        codebook = {}
    if node.char is not None:
        codebook[node.char] = prefix
    else:
        build_code_table(node.left, prefix + "0", codebook)
        build_code_table(node.right, prefix + "1", codebook)
    return codebook

def encode_string_with_codes(s: str, codes: dict[str, str]) -> tuple[bytes, int]:
    """Encode the string into Huffman bitstream."""
    bitstring = ''.join(codes[char] for char in s)
    bit_len = len(bitstring)
    padding = (8 - bit_len % 8) % 8
    bitstring_padded = bitstring + '0' * padding

    encoded_bytes = bytearray()
    for i in range(0, len(bitstring_padded), 8):
        encoded_bytes.append(int(bitstring_padded[i:i+8], 2))

    return bytes(encoded_bytes), bit_len

def build_huffman_package(codes: dict[str, str], original_string: str) -> bytes:
    """Create a binary blob containing the Huffman codebook and the encoded string."""
    buffer = bytearray()

    # Encode the input string
    encoded_data, bit_length = encode_string_with_codes(original_string, codes)

    # 1. Write number of codebook entries
    buffer.extend(len(codes).to_bytes(2, 'big'))

    # 2. Write each codebook entry
    for char, code in codes.items():
        utf8_bytes = char.encode('utf-8')
        code_len = len(code)

        # Pad the code to full byte
        padding = (8 - code_len % 8) % 8
        code_padded = code + '0' * padding
        code_bytes = bytearray()
        for i in range(0, len(code_padded), 8):
            code_bytes.append(int(code_padded[i:i+8], 2))

        buffer.append(len(utf8_bytes))  # 1 byte: UTF-8 byte length
        buffer.extend(utf8_bytes)       # N bytes: UTF-8 bytes
        buffer.append(code_len)         # 1 byte: bit length
        buffer.extend(code_bytes)       # M bytes: actual bits

    # 3. Write bitstream length (4 bytes)
    buffer.extend(bit_length.to_bytes(4, 'big'))

    # 4. Write encoded data
    buffer.extend(encoded_data)

    return bytes(buffer)

def decode_huffman_package(data: bytes) -> bytes:
    pos = 0

    # 1. Number of codebook entries (2 bytes)
    num_entries = int.from_bytes(data[pos:pos+2], 'big')
    pos += 2

    codes = {}

    # 2. Read each codebook entry
    for _ in range(num_entries):
        char_len = data[pos]
        pos += 1

        char_bytes = data[pos:pos+char_len]
        pos += char_len

        code_bit_len = data[pos]
        pos += 1

        code_byte_len = math.ceil(code_bit_len / 8)
        code_bytes = data[pos:pos+code_byte_len]
        pos += code_byte_len

        bit_str = ''.join(f'{b:08b}' for b in code_bytes)
        code = bit_str[:code_bit_len]

        codes[char_bytes] = code  # Store UTF-8 bytes directly as key

    # 3. Encoded bitstream length (4 bytes)
    bitstream_len = int.from_bytes(data[pos:pos+4], 'big')
    pos += 4

    # 4. Read and decode bitstream
    bitstream_bytes = data[pos:]
    bitstream_bits = ''.join(f'{b:08b}' for b in bitstream_bytes)[:bitstream_len]

    reverse_codes = {v: k for k, v in codes.items()}

    decoded = bytearray()
    buffer = ''
    for bit in bitstream_bits:
        buffer += bit
        if buffer in reverse_codes:
            decoded.extend(reverse_codes[buffer])
            buffer = ''

    return bytes(decoded)

def write_file(data: bytes, file_path: str):
    with open(file_path, 'wb') as f:
        f.write(data)

def read_file(file_path: str) -> bytes:
    with open(file_path, 'rb') as f:
        return f.read()