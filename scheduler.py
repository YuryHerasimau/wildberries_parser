# Выполнять: регулярно по расписанию (достаточно предложить и описать метод запуска)

# На Linux: проще всего использовать crontab
# На Windows: создать исполняемый bat-файл и запускать его через планировщик
# Также можно использовать библиотеку schedule, redis и тд

import schedule
from wb_parser import main as parse_on_schedule


def main():
    print("It's already 09:00 AM. Let's parse WildBerries!")
    schedule.every().day.at('09:00').do(parse_on_schedule)

    try:
        while True:
            schedule.run_pending()
    except KeyboardInterrupt:
        exit()


if __name__ == "__main__":
    main()