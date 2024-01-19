def parse_from_path(path) -> dict():
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    sections = content.split('[')




