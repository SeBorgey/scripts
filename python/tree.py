import os


def print_directory_contents(directory, level=0):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        indent = "    " * level

        if os.path.isfile(file_path):
            if filename.endswith(".tgz"):
                print(f"{indent}├── {filename}")
            else:
                print(f"{indent}├── {filename}")
                with open(file_path, "r") as file:
                    content = file.read()
                    print(f"{indent}    {content}")
        else:
            print(f"{indent}├── {filename}/")
            print_directory_contents(file_path, level + 1)



root_directory = ("/home/kaneki/Vocabular_web")

print_directory_contents(root_directory)