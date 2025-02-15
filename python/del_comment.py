import os


def remove_comments_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    cleaned_lines = []
    for line in lines:
        if '#' in line:
            stripped_line = line.split('#')[0].rstrip()
            cleaned_lines.append(stripped_line + '\n')
        else:
            cleaned_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(cleaned_lines)


def remove_comments_from_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d != '.venv']
        for file_name in files:
            if file_name.endswith('.py'):
                file_path = os.path.join(root, file_name)
                remove_comments_from_file(file_path)
                print(f'Обработан файл: {file_path}')


if __name__ == "__main__":
    folder = "/home/kaneki/Documents/prog_3sem/formal/interpret"
    if os.path.isdir(folder):
        remove_comments_from_folder(folder)
        print("Удаление комментариев завершено.")
    else:
        print("Указанный путь не является папкой.")
