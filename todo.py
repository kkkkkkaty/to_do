import json
import os

STORAGE = "data.db"

def read_storage():
    if os.path.exists(STORAGE):
        try:
            with open(STORAGE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def write_storage(records):
    try:
        with open(STORAGE, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    except:
        pass

def new_record(records):
    txt = input("Введите текст: ").strip()
    if not txt:
        return records
    
    if records:
        nid = max(r['id'] for r in records) + 1
    else:
        nid = 1
    
    rec = {'id': nid, 'txt': txt, 'stat': False}
    records.append(rec)
    write_storage(records)
    print(f"Запись #{nid} добавлена")
    return records

def view_records(records):
    if not records:
        print("Нет записей")
        return
    
    print("\nСписок записей:")
    for r in records:
        mark = "[Г]" if r['stat'] else "[Н]"
        print(f"{r['id']}. {mark} {r['txt']}")

def change_stat(records):
    try:
        rid = int(input("ID записи: "))
        for r in records:
            if r['id'] == rid:
                r['stat'] = True
                write_storage(records)
                print(f"Запись #{rid} обновлена")
                return records
        print(f"Запись #{rid} не найдена")
    except:
        print("Ошибка ввода")
    return records

def erase_record(records):
    try:
        rid = int(input("ID для удаления: "))
        new_recs = [r for r in records if r['id'] != rid]
        if len(new_recs) == len(records):
            print(f"Запись #{rid} не найдена")
        else:
            write_storage(new_recs)
            print(f"Запись #{rid} удалена")
            return new_recs
    except:
        print("Ошибка ввода")
    return records

def show_interface():
    print("\n" + "=" * 35)
    print("Управление записями")
    print("=" * 35)
    print("1. Новая запись")
    print("2. Показать записи")
    print("3. Изменить статус")
    print("4. Удалить запись")
    print("5. Выход")
    print("=" * 35)

def controller():
    print("Загрузка системы...")
    recs = read_storage()
    
    while True:
        show_interface()
        
        try:
            cmd = input("Команда (1-5): ").strip()
            
            if cmd == "1":
                recs = new_record(recs)
            elif cmd == "2":
                view_records(recs)
            elif cmd == "3":
                recs = change_stat(recs)
            elif cmd == "4":
                recs = erase_record(recs)
            elif cmd == "5":
                print("Завершение работы")
                break
            else:
                print("Неверная команда")
                
        except KeyboardInterrupt:
            print("\nРабота прервана")
            break
        except Exception as err:
            print(f"Системная ошибка: {err}")

if __name__ == "__main__":
    controller()