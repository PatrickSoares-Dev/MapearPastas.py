import os
import json
from datetime import datetime

# Lista de pastas a serem ignoradas
IGNORED_FOLDERS = {'.git', 'node_modules', '.vs', 'bin', 'obj', '__pycache__'}

def map_directory(directory):
    directory_structure = {"name": os.path.basename(directory), "path": directory, "children": []}
    
    items = os.listdir(directory)
    items.sort()  # Ordenar itens alfabeticamente para melhor organização
    
    for item in items:
        full_path = os.path.join(directory, item)
        
        if os.path.isdir(full_path):
            if item not in IGNORED_FOLDERS:
                directory_structure["children"].append(map_directory(full_path))
        else:
            directory_structure["children"].append({"name": item, "path": full_path})
    
    return directory_structure

if __name__ == "__main__":
    directory_to_map = input("Digite o diretório que você quer mapear: ")
    
    if os.path.exists(directory_to_map) and os.path.isdir(directory_to_map):
        mapped_structure = map_directory(directory_to_map)
        
        # Criar um diretório para armazenar o arquivo JSON
        output_dir = "mapped_directories"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Criar um subdiretório com o nome e data
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        sub_dir_name = f"{os.path.basename(directory_to_map)}_{current_time}"
        sub_dir_path = os.path.join(output_dir, sub_dir_name)
        os.makedirs(sub_dir_path)
        
        # Salvar o arquivo JSON
        json_file_path = os.path.join(sub_dir_path, "directory_structure.json")
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(mapped_structure, json_file, ensure_ascii=False, indent=4)
        
        print(f"Estrutura do diretório salva em: {json_file_path}")
    else:
        print(f"O diretório '{directory_to_map}' não existe ou não é um diretório válido.")