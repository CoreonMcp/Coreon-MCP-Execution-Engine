from service.prompt import generate_final_system_prompt
from typing import List, Dict
from service.llm import parse_input_to_toolcalls

class MCPPlanner:
    def __init__(self):
        self.system_prompt = generate_final_system_prompt()

    def plan(self, user_input: str) -> List[Dict]:
        return parse_input_to_toolcalls(user_input, self.system_prompt)

