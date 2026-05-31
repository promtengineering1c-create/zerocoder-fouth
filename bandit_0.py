import os
import paramiko
from dotenv import load_dotenv

def start_interactive_shell(level, password):
    try:
        client.connect(
            hostname=BANDIT_HOST, 
            port=BANDIT_PORT, 
            username=f"bandit{level}", 
            password=password
        )
        print(f"\n=== УСПЕШНОЕ ПРЯМОЕ ПОДКЛЮЧЕНИЕ К LEVEL {level} ===")
        print("Для выхода введи 'exit'\n")

    except Exception as e:
        print(f"Не удалось подключиться к уровню {level}: {e}")

def interactive_mode(level):
    print(f"\nПереход в ручной режим (Level {level}). Введи 'exit', чтобы выйти из терминала и продолжить скрипт.")
    while True:
        command = input(f"bandit{level}@labs:~$ ")
        if command.strip().lower() == 'exit':
            break
        if not command.strip():
            continue
        
        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read().decode('utf-8') + stderr.read().decode('utf-8'), end="")

def handle_level_completed(stdout, stderr, level):
        # Читаем ответ и очищаем его от лишних пробелов
    BANDIT_PASSWORD = stdout.read().decode('utf-8').strip()
    print(BANDIT_PASSWORD)
    error = stderr.read().decode('utf-8')
    print(error)
     
    user_choice = input(f"Перейти на уровень {level + 1}? (y/n): ")

    if user_choice.strip().lower() == 'y':
        print("Продожаем игру...")
    
        if error:
            print(f"Ошибка при чтении файла: {error}")
        elif BANDIT_PASSWORD:
            # Увеличиваем уровень на 1
            level += 1
            print(f"Найден пароль для уровня {level}: {BANDIT_PASSWORD}")
            
            # Формируем имя ключа, например "BANDIT1"
            next_bandit_key = f"BANDIT{level}"
            
            with open(ENV_FILE, "a", encoding="utf-8") as f:
                f.write(f"{next_bandit_key}={BANDIT_PASSWORD}\n")
            print(f"💾 Пароль {next_bandit_key} успешно сохранен в файл .env!")

            found_passwords[level] = BANDIT_PASSWORD

            start_interactive_shell(level, BANDIT_PASSWORD)
    else:
        print("Отмена перехода на следующий уровень. Соединение оставлено открытым.")
        interactive_mode(level)

    return level

ENV_FILE = ".env"

default_settings = {
    "BANDIT_HOST": "bandit.labs.overthewire.org",
    "BANDIT_PORT": "2220",
    "BANDIT0": "bandit0"
}

if not os.path.exists(ENV_FILE):
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        pass

existing_lines = []
existing_keys = set()
found_passwords = {}  # Словарь для хранения найденных паролей в формате {уровень: пароль}

with open(ENV_FILE, "r", encoding="utf-8") as f:
    for line in f:
        existing_lines.append(line)
        clean_line = line.strip()
        
        if clean_line and not clean_line.startswith("#") and "=" in clean_line:
            key, value = clean_line.split("=", 1)
            key = key.strip()
            existing_keys.add(key)
            
            if key.startswith("BANDIT") and key[6:].isdigit():
                level_num = int(key[6:])
                found_passwords[level_num] = value.strip()

missing_settings = []
for key, value in default_settings.items():
    if key not in existing_keys:
        missing_settings.append(f"{key}={value}\n")
        if key == "BANDIT0":
            found_passwords[0] = value

if missing_settings:
    with open(ENV_FILE, "a", encoding="utf-8") as f:
        if existing_lines and not existing_lines[-1].endswith("\n"):
            f.write("\n")
        f.writelines(missing_settings)
    print(f"В {ENV_FILE} добавлены недостающие переменные.")

LEVEL = max(found_passwords.keys()) if found_passwords else 0
BANDIT_PASSWORD = found_passwords.get(LEVEL)

load_dotenv()

BANDIT_HOST = os.getenv("BANDIT_HOST", "bandit.labs.overthewire.org")
BANDIT_PORT = int(os.getenv("BANDIT_PORT", 2220))

print(f"Автоопределение: продолжаем игру с Bandit Level {LEVEL}")

if not BANDIT_PASSWORD:
    print(f"Ошибка: Пароль для BANDIT{LEVEL} не определен!")
    exit()

print(f"Подключаемся НАПРЯМУЮ к Bandit Level {LEVEL}...")


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

start_interactive_shell(LEVEL, BANDIT_PASSWORD)

if LEVEL == 0:
    print(f"Пытаемся автоматически найти пароль для Level {LEVEL + 1}...")
    stdin, stdout, stderr = client.exec_command("cat readme")

    LEVEL = handle_level_completed(stdout, stderr, LEVEL)
   
if LEVEL == 1:
    print(f"Пытаемся автоматически найти пароль для Level {LEVEL + 1}...")
    stdin, stdout, stderr = client.exec_command("cat ./- | awk '{print $NF}'")
    
    LEVEL = handle_level_completed(stdout, stderr, LEVEL)    
     
if LEVEL == 2:
    print(f"Пытаемся автоматически найти пароль для Level {LEVEL + 1}...")
    stdin, stdout, stderr = client.exec_command("cat ./'--spaces in this filename--'")
    
    LEVEL = handle_level_completed(stdout, stderr, LEVEL)
     
if LEVEL == 3:
    print(f"Пытаемся автоматически найти пароль для Level {LEVEL + 1}...")
    stdin, stdout, stderr = client.exec_command("cd ./inhere/ && cat ./.*")
    
    LEVEL = handle_level_completed(stdout, stderr, LEVEL)
   
if LEVEL == 4:
    print(f"Пытаемся автоматически найти пароль для Level {LEVEL + 1}...")
    stdin, stdout, stderr = client.exec_command("cd ./inhere/ && file ./*")
    lines = stdout.readlines()
    for line in lines:
        if "ASCII text" in line:
            file_name = line.split(":")[0].strip()
            stdin, stdout, stderr = client.exec_command(f"cd ./inhere/ && cat {file_name}")
            break    
    
    LEVEL = handle_level_completed(stdout, stderr, LEVEL)
    
if LEVEL == 5:
    print(f"Пытаемся автоматически найти пароль для Level {LEVEL + 1}...")
    stdin, stdout, stderr = client.exec_command("cd ./inhere/ && find -size 1033c -type f ! -executable")
    file_name = stdout.read().decode('utf-8').strip()
    stdin, stdout, stderr = client.exec_command(f"cd ./inhere/ && cat {file_name}")
        
    LEVEL = handle_level_completed(stdout, stderr, LEVEL)

if LEVEL == 6:
    print(f"Пытаемся автоматически найти пароль для Level {LEVEL + 1}...")
    stdin, stdout, stderr = client.exec_command("find / -size 33c -type f -user bandit7 -group bandit6 2> /dev/null")
    file_name = stdout.read().decode('utf-8').strip()
    stdin, stdout, stderr = client.exec_command(f"cat {file_name}")
        
    LEVEL = handle_level_completed(stdout, stderr, LEVEL)

if LEVEL == 7:
    print(f"Пытаемся автоматически найти пароль для Level {LEVEL + 1}...")
    stdin, stdout, stderr = client.exec_command("grep 'millionth' data.txt | awk '{print $2}'")
                
    LEVEL = handle_level_completed(stdout, stderr, LEVEL)

if LEVEL == 8:
    print(f"Пытаемся автоматически найти пароль для Level {LEVEL + 1}...")
    stdin, stdout, stderr = client.exec_command("sort data.txt | uniq -u")
                
    LEVEL = handle_level_completed(stdout, stderr, LEVEL) 

if LEVEL == 9:
    print(f"Пытаемся автоматически найти пароль для Level {LEVEL + 1}...")
    stdin, stdout, stderr = client.exec_command("strings data.txt | grep '====' | tail -n 1 | awk '{print $NF}'")
                
    LEVEL = handle_level_completed(stdout, stderr, LEVEL) 

if LEVEL == 10:
    print(f"Пытаемся автоматически найти пароль для Level {LEVEL + 1}...")
    stdin, stdout, stderr = client.exec_command("base64 -d data.txt | awk '{print $NF}'")
                
    LEVEL = handle_level_completed(stdout, stderr, LEVEL)             

user_choice = input("🔌 Завершить работу и закрыть соединение? (y/n): ")

if user_choice.strip().lower() == 'y':
    print("Закрываем соединение...")
    client.close()
else:
    print("Соединение оставлено открытым. Скрипт завершен.")
    interactive_mode(LEVEL)