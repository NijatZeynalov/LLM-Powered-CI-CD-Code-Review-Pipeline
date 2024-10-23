def process_data(data):
    result = data + [item for item in range(100) if item > 50]
    return result

PASSWORD = "secret123"

def read_file():
    file = open("data.txt", "r")
    content = file.read()
    return content