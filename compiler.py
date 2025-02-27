import os

def get_project_structure(root_dir, ignore_dirs):
    """Genera la estructura del proyecto en forma de árbol de directorios, ignorando ciertos directorios."""
    structure = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]  # Filtrar directorios ignorados
        level = dirpath.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        structure.append(f"{indent}[{os.path.basename(dirpath)}]")
        sub_indent = ' ' * 4 * (level + 1)
        for filename in filenames:
            structure.append(f"{sub_indent}- {filename}")
    return "\n".join(structure)

def read_project_files(root_dir, output_file, ignore_dirs, ignore_files, image_extensions):
    """Lee todos los archivos del proyecto y los guarda en un archivo de texto, ignorando ciertos directorios y archivos."""
    with open(output_file, 'w', encoding='utf-8') as out_file:
        # Escribir la estructura del proyecto
        out_file.write("Estructura del Proyecto:\n")
        out_file.write(get_project_structure(root_dir, ignore_dirs) + "\n\n")
        
        for dirpath, _, filenames in os.walk(root_dir):
            if any(ignored in dirpath.split(os.sep) for ignored in ignore_dirs):
                continue  # Saltar directorios ignorados
            
            filenames = [f for f in filenames if f not in ignore_files]  # Filtrar archivos ignorados
            
            if filenames:
                folder_name = os.path.relpath(dirpath, root_dir)
                out_file.write(f"===={folder_name}====\n")
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    
                    if any(filename.lower().endswith(ext) for ext in image_extensions):
                        out_file.write(f"\n--- {filename} (imagen) ---\n")
                        continue  # Solo escribir el nombre de la imagen
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            content = file.read()
                            out_file.write(f"\n--- {filename} ---\n")
                            out_file.write(content + "\n")
                    except Exception as e:
                        out_file.write(f"\n--- {filename} ---\nError al leer el archivo: {e}\n")
                out_file.write("\n")

if __name__ == "__main__":
    proyecto_path = os.path.abspath(".")  # Directorio actual como referencia
    output_filename = "proyecto_completo.txt"
    ignore_dirs = {"venv", ".vscode", "__pycache__", ".git"}  # Directorios a ignorar
    ignore_files = {"session.json", ".gitignore", "README.md", "bg_rc.py", "compiler.py"}  # Archivos a ignorar
    image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg"}  # Extensiones de imágenes
    read_project_files(proyecto_path, output_filename, ignore_dirs, ignore_files, image_extensions)
    print(f"Archivo '{output_filename}' generado correctamente.")
