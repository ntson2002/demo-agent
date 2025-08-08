import json
from openai import OpenAI
from dotenv import load_dotenv
from modules.utils import cprint
from modules.tools import get_stock_price, get_student_info, calculate, get_current_weather, tool_descriptions
load_dotenv()


class SimpleAgent:
    def __init__(self, system_instruction=None):
        self.client = OpenAI()
        self.history = []
        self.system_instruction = system_instruction or "Bạn là một AI assistant thông minh có khả năng cung cấp thông tin thời tiết, thông tin sinh viên và thực hiện các phép tính toán. Hãy trả lời bằng tiếng Việt và cố gắng hữu ích nhất có thể."
        self.tools = tool_descriptions 
        self.available_functions = {
            "get_current_weather":get_current_weather,
            "get_stock_price": get_stock_price,
            "get_student_info": get_student_info,
            "calculate": calculate
        }

    def run_conversation(self, prompt):
        # Step 1: send the conversation and available functions to the model
        messages = [{"role": "system", "content": self.system_instruction}]
        
        # Thêm lịch sử chat vào messages
        messages.extend(self.history)
        
        # Thêm message hiện tại
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=self.tools,
            tool_choice="auto",  # auto is default, but we'll be explicit
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        
        # Lưu user message vào history
        self.history.append({"role": "user", "content": prompt})
        
        # print(response_message)
        # Step 2: check if the model wanted to call a function
        if tool_calls:
            
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            messages.append(response_message)  # extend conversation with assistant's reply
            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                
                function_to_call = self.available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                cprint(f"\n🤖 Agent đang gọi tool {function_name} với tham số {function_args}...", color="blue")
                # print(function_to_call)
                # print(function_args)
                function_response = function_to_call(**function_args)
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response
            second_response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )  # get a new response from the model where it can see the function response

            # Lưu assistant response vào history
            self.history.append({"role": "assistant", "content": second_response.choices[0].message.content})
            return second_response
        
        # Lưu assistant response vào history
        self.history.append({"role": "assistant", "content": response_message.content})
        return response

hello_world = """
====================================================
============🌤️      SimpleAgent Chat    =============
====================================================
👋 Chào mừng! Tôi là SimpleAgent, có thể giúp bạn:
- Kiểm tra thời tiết
- Lấy giá cổ phiếu
- Tìm thông tin sinh viên
- Thực hiện các phép tính
Gõ 'exit' để thoát
====================================================
"""
if __name__ == "__main__":
    agent = SimpleAgent()
    print(hello_world)
    while True:
        try:
            user_input = input("\n👤 Bạn: ").strip()
            
            if user_input.lower() == 'exit':
                cprint("👋 Tạm biệt! Hẹn gặp lại! 👋", color="green")
                break
                
            if not user_input:
                print("⚠️  Vui lòng nhập tin nhắn!")
                continue
                
            cprint("\n🤖 Agent đang xử lý...", color="blue")
            response = agent.run_conversation(user_input)
            cprint(f"\n🤖 Agent: {response.choices[0].message.content}", color="magenta")
            
        except KeyboardInterrupt:
            cprint("\n\n👋 Tạm biệt! Hẹn gặp lại! 👋", color="green")
            break
        except Exception as e:
            cprint(f"❌ Lỗi: {e}", color="red")
            cprint("🔄 Vui lòng thử lại!", color="red")