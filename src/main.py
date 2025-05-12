import argparse
from csv_reader import read_list_csv
from env_setting import REPORT_CHOICES
from report_generate import print_payouts_report


def main():
    parser = argparse.ArgumentParser(
        description="Обработка имен CSV-файлов с командной строки"
    )
    parser.add_argument("files", nargs="+", help="Список имен CSV-файлов")
    parser.add_argument(
        "--report", choices=REPORT_CHOICES, required=True, help="Тип отчета"
    )
    args = parser.parse_args()
    all_data_employers = read_list_csv(args.files)

    if args.report == "payout":
        print_payouts_report(all_data_employers)


if __name__ == "__main__":
    main()
