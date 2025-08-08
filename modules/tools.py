import json 

def get_student_info(student_id):
    """Lấy thông tin sinh viên dựa trên mã số sinh viên
    Args:
        student_id: Mã số sinh viên
    Returns:
        Thông tin sinh viên
    """
    # print("student_id", student_id)
    student_dic = {'123456': {'name': "Nguyễn Trường Sơn", "email": "ntson@fit.hcmus.edu.vn"},
                   '123457': {'name': "Trần Thu Hà"}}
    return json.dumps(student_dic.get(student_id, {"result": "Not found !"}))

def calculate(a, b, operator):
    """Tính toán giá trị dựa trên hai số và một phép toán
    Args:
        a: Số thứ nhất
        b: Số thứ hai
        operator: Phép toán (+, -, *, /)
    Returns:
        Kết quả tính toán
    """
    # print(a, b, operator)
    if operator == '+':
        r = a + b
    elif operator == '-':
        r = a - b
    elif operator == '*':
        r = a * b
    elif operator == '/':
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        r = a / b
    else:
        raise ValueError("Invalid operator. Please use one of the following: +, -, *, /")
    return json.dumps({"result": r}, ensure_ascii=False)

def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location
    Args:
        location: Tên thành phố
        unit: Đơn vị đo nhiệt độ (fahrenheit, celsius)
    Returns:
        Thông tin thời tiết
    """
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})

def get_stock_price(stock_symbol):
        # print("stock_symbol", stock_symbol)
        stock_price = {'AAPL': 150.75, 'GOOG': 2800.12, 'MSFT': 235.22, 'BID': 38000, 'VCB': 54000, 'TCBS': 10000}
        return json.dumps({"stock_symbol": stock_symbol, "price": stock_price.get(stock_symbol, "Not found !")})

# Dictionary chứa các hàm có sẵn
available_functions = {
    "get_current_weather": get_current_weather,
    "get_student_info": get_student_info,
    "calculate": calculate,
    "get_stock_price": get_stock_price
}

tool_descriptions = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
    },
    {
            "type": "function",
            "function": {
                "name": "get_student_info",
                "description": "Lấy thông tin sinh viên dựa trên mã số sinh viên",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "student_id": {
                            "type": "string",
                            "description": "Mã số sinh viên, ví dụ: 'SV123456'"
                }
                },
                "required": ["student_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Tính toán giá trị dựa trên hai số và một phép toán",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "Số thứ nhất, ví dụ: 5"
                    },
                    "b": {
                        "type": "number",
                        "description": "Số thứ hai, ví dụ: 3"
                    },
                    "operator": {
                        "type": "string",
                        "enum": ["+", "-", "*", "/"],
                        "description": "Phép toán cần thực hiện: +, -, *, /"
                    }
                },
                "required": ["a", "b", "operator"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Lấy giá cổ phiếu của một công ty dựa trên mã cổ phiếu",
            "parameters": {
                "type": "object",
                "properties": {
                    "stock_symbol": {
                        "type": "string",
                        "description": "Mã cổ phiếu, ví dụ: ngân hàng BIDV --> BID, ngân hàng Vietcombank --> VCB, ngân hàng Techcombank --> TCBS"
                    }
                },
                "required": ["stock_symbol"]
            }
        }
    }
]

# Test các hàm
if __name__ == "__main__":
    from modules.utils import function_to_json
    
    print("=== Test các hàm ===")
    print(json.dumps(function_to_json(get_student_info), ensure_ascii=False, indent=4))
    print(json.dumps(function_to_json(calculate), ensure_ascii=False, indent=4))
    print(json.dumps(function_to_json(get_current_weather), ensure_ascii=False, indent=4))
    
    print("\n=== Test chức năng ===")
    print("Thông tin sinh viên:", get_student_info("123456"))
    print("Tính toán:", calculate(10, 5, "+"))
    print("Thời tiết:", get_current_weather("Tokyo", "celsius"))