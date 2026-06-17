def process_file(input_file, output_file, key):

    with open(input_file, 'rb') as f:
        data = f.read()

    result = bytearray()
    for byte in data:
        rotated = ((byte << 2) | (byte >> 6)) & 0xFF
        result.append(rotated ^ key)

    with open(output_file, 'wb') as f:
        f.write(result)

    print(f"Готово! Файл сохранен: {output_file}")


print("1 - Зашифровать")
print("2 - Расшифровать")
choice = input("Выберите действие: ")

input_file = input("Введите путь к файлу: ")
output_file = input("Введите путь для сохранения: ")
key = int(input("Введите ключ (0-255): "))

if 0 <= key <= 255:
    process_file(input_file, output_file, key)
else:
    print("Ключ должен быть от 0 до 255!")