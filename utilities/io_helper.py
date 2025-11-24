import csv

import json

import os

class IOHelper:

    @staticmethod
    def read_txt_file_to_list(filepath: str) -> list[str] | None:
        
        lines: list[str] = None
        
        with open(filepath, "r") as txt_file:
            lines = txt_file.readlines()
        
        return lines
    
    @staticmethod
    def write_line_to_txt_file(
        filepath: str,
        line: str,
        mode: str = "w") -> None:

        with open(filepath, mode=mode) as txt_file:
            txt_file.write(f"{line}\n")
    
    @staticmethod
    def read_rows_from_csv_file(
        filepath: str,
        has_headers: bool) -> tuple[list[list[str]], list[str] | None]:

        rows: list[list[str]] = None
        headers: list[str] = None
        
        if has_headers:
            has_processed_headers: bool = False
        else:
            has_processed_headers: bool = True

        with open(filepath,"r",newline='') as csv_file:
            
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                
                if not has_processed_headers:
                    headers = row
                    has_processed_headers = True
                else:
                    rows.append(row)
        
        return rows, headers
    
    @staticmethod
    def write_dict_to_json_file(
        data: dict,
        filepath: str,
        mode: str = "w"):

        with open(filepath, mode) as json_file:
            json.dump(data, json_file)
    
    @staticmethod
    def read_dict_from_local_json_file(json_filepath: str) -> dict | None:

        try:
            data: dict = None

            with open(json_filepath, "r") as json_file:
                data = json.load(json_file)
        
            return data
        
        except FileNotFoundError:

            return None

    @staticmethod
    def write_list_to_csv_file(
        filepath: str,
        list_arg: list,
        mode: str = "a"):

        with open(filepath, mode=mode, newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(list_arg)
    
    @staticmethod
    def write_lists_to_csv_file(
        filepath: str,
        lists_arg: list[list],
        mode: str = "a"):

        with open(filepath, mode=mode, newline="") as csv_file:
            
            writer = csv.writer(csv_file, delimiter=',')

            for list_arg in lists_arg:
                writer.writerow(list_arg)

    @staticmethod
    def delete_local_file(filepath: str):

        if os.path.exists(filepath):
            os.remove(filepath)

    @staticmethod
    def read_csv_file_to_lists(filepath: str):

        rows: list[list] = []

        with open(filepath, mode="r", newline="") as csv_file:
            
            reader = csv.reader(csv_file, delimiter=",")
            
            for row in reader:
                rows.append(row)
        
        return rows





