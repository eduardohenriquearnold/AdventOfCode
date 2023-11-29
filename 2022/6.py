
def get_start_marker(input_string: str, marker_size: int) -> int:
    for i in range(marker_size, len(input_string)-marker_size+1):
        substr = input_string[i-marker_size:i]
        if len(set(substr)) == marker_size:
            return i


input_string = open('inputs/6.txt').read()
print(get_start_marker(input_string, 4))
print(get_start_marker(input_string, 14))