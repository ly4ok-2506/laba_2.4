import struct
import os


def generate_initial_file(filepath):
    test_numbers = [1, 14, 21, 30, 67, 70]
    with open(filepath, 'wb') as f:
        for num in test_numbers:
            f.write(struct.pack('<i', num))
    print(f"Создан исходный файл {filepath} с числами: {test_numbers}")


def print_file_content(filepath, message="Содержимое файла:"):
    numbers = []
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(4)
            if not chunk or len(chunk) < 4:
                break
            numbers.append(struct.unpack('<i', chunk)[0])
    print(f"{message} {numbers}")


def process_file_inplace(filepath):
    divisor = 73 ** 2 + 29

    with open(filepath, 'r+b') as f:
        while True:
            current_position = f.tell()

            chunk = f.read(4)
            if not chunk or len(chunk) < 4:
                break

            value = struct.unpack('<i', chunk)[0]

            if value % 7 == 0:
                new_value = int(value * 100 / divisor)

                f.seek(current_position)

                f.write(struct.pack('<i', new_value))

                f.seek(current_position + 4)


if __name__ == "__main__":
    os.makedirs('resource', exist_ok=True)
    bin_file = 'resource/numbers.bin'

    generate_initial_file(bin_file)

    print_file_content(bin_file, "Числа ДО обработки:  ")

    process_file_inplace(bin_file)

    print_file_content(bin_file, "Числа ПОСЛЕ обработки:")