import re
import os
import pandas as pd
from server import PromptServer
from aiohttp import web

prompts_path = os.path.abspath(os.path.join(__file__, "../CSV")) 
############################################  Async get header and colum

### Read the first column of CSV ###
@PromptServer.instance.routes.get("/pysssss/first_column/{name}")  
async def get_first_column_api(request):
    name = request.match_info["name"]
    name = name.replace("⧵", "/")
    csv_path = os.path.abspath(os.path.join(__file__, "../CSV/", name))

    if not os.path.exists(csv_path):
        print(f"Error. No .csv file found.")
        return web.json_response(["Error: File Not Found"])

    try:
        df = pd.read_csv(csv_path, delimiter=';', encoding='utf-8')
        # Generate "rowName_index, for example rowName1_1". This is to make sure the key of the dict is unique.
        first_column_list = [f"{value}_{idx}" for idx, value in enumerate(df.iloc[:, 0])]
    except Exception as e:
        print(f"Error loading .csv file (Front). Error: {e}")
        return web.json_response(["Error: Unable to Read File"])

    if not first_column_list:
        first_column_list = ["[none]"]
    
    return web.json_response(first_column_list)


### Read the first row of CSV ###
@PromptServer.instance.routes.get("/pysssss/first_row/{name}")  
async def get_first_row_api(request):
    name = request.match_info["name"]
    name = name.replace("⧵", "/")
    csv_path = os.path.abspath(os.path.join(__file__, "../CSV/", name))

    if not os.path.exists(csv_path):
        print(f"Error. No .csv file found.")
        return web.json_response(["Error: File Not Found"])

    try:
        df = pd.read_csv(csv_path, delimiter=';', encoding='utf-8')
        # Generate "columnName_index, for example columnName1_1". This is to make sure the key of the dict is unique.
        first_row_list = [f"{col}_{idx}" for idx, col in enumerate(df.columns)]
    except Exception as e:
        print(f"Error loading columns. Error: {e}")
        return web.json_response(["Error: Unable to Read Columns"])

    if not first_row_list:
        first_row_list = ["[none]"]  

    return web.json_response(first_row_list)


###########################################################################




########################################
class TextFileNode:
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("value",)
    CATEGORY = "Custom CSV Loader Node"

    @classmethod
    def VALIDATE_INPUTS(self, column, row):
        if column == "[none]" or not column or not column.strip(): 
            return True #Always validate if nothing is selected
        if row == "[none]" or not row or not row.strip(): 
            return True #Always validate if nothing is selected
        return True

    def load_text(self, column, row, csv_file): #execution is here
        csv_path = os.path.abspath(os.path.join(__file__, "../CSV/", csv_file))
        index_row = self.get_csv_first_column(csv_path).get(row)
        index_column = self.get_csv_first_row(csv_path).get(column)
        print(f"index_row : {index_row}")
        print(f"index_column : {index_column}")
        output = self.get_csv_value(csv_path, index_row, index_column) + ","
        return (output,)
###############################################


class CSVLoader(TextFileNode):
    """
    Loads csv file with artists.
    """
    @staticmethod
    def get_csv_first_row(file_path):
        df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')
        first_row_dict = {f"{value}_{idx}": idx if pd.notna(value) else f"Unknown_{idx}" 
                    for idx, value in enumerate(df.columns)}

        return first_row_dict

    @staticmethod
    def get_csv_first_column(file_path):
        df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')
        first_column_dict = {f"{value}_{idx}": idx if pd.notna(value) else f"Unknown_{idx}"
                            for idx, value in enumerate(df.iloc[:, 0])}


        return first_column_dict

    @staticmethod
    def get_csv_value(file_path, n, m):
        """
        Read the content from the n row and m column in a CSV file.
        
        """

        # print(f"file_path : {file_path}")
        # print(f"m : {m}")
        # print(f"n : {n}")

        try:
            # Load CSV
            df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')  # 可以改成 `delimiter=';'` 适配不同格式

            # Check if out fo index
            if n >= len(df) or m >= len(df.columns):
                return "Out of Index"

            value = df.iloc[n, m]  # Get the value from n row and m column

            print(f"output in get_csv_value: {str(value)}")
            return str(value)

        except Exception as e:
            return f"ERROR:get_csv_value: {e}"

    @classmethod
    def IS_CHANGED(self):
        return float("nan")

    @classmethod
    def INPUT_TYPES(cls):

#File input
        global prompts_path  
        try:
            prompt_files = []
            for root, dirs, files in os.walk(prompts_path):  
                for file in files:
                    if file.endswith(".csv"):  
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, prompts_path)
                        rel_path = rel_path.replace("\\", "⧵")  
                        prompt_files.append(rel_path)
        except Exception:
            prompt_files = []
##########

        return {
            "required": {
                "csv_file": (prompt_files,),  # Select CSV
                "row": (["[none]"], {  # Default ["[none]"]，refresh when dynamic loading
                    "pysssss.binding": [{  
                        "source": "csv_file",  
                        "callback": [{
                            "type": "set",
                            "target": "$this.disabled",  
                            "value": True
                        }, {
                            "type": "fetch",
                            "url": "/pysssss/first_column/{$source.value}",  
                            "then": [{
                                "type": "set",
                                "target": "$this.options.values",
                                "value": "$result"
                            }, 
                            {
                                "type": "validate-combo"
                            }, 
                            {
                                "type": "set",
                                "target": "$this.disabled",  
                                "value": False
                            }]
                        }],
                    }]
                }),
                "column": (["[none]"], {  # Default ["[none]"]，refresh when dynamic loading
                    "pysssss.binding": [{  
                        "source": "csv_file",  
                        "callback": [{
                            "type": "set",
                            "target": "$this.disabled",  
                            "value": True
                        }, {
                            "type": "fetch",
                            "url": "/pysssss/first_row/{$source.value}",  
                            "then": [{
                                "type": "set",
                                "target": "$this.options.values",
                                "value": "$result"
                            }, {
                                "type": "validate-combo"
                            }, {
                                "type": "set",
                                "target": "$this.disabled",  
                                "value": False
                            }]
                        }],
                    }]
                })
            },
        }


    FUNCTION = "load_text"


NODE_CLASS_MAPPINGS = {
    "Custom CSV Loader": CSVLoader,


}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Custom CSVLoader": "Custom CSV Loader Node", 
}