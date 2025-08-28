import importlib
import yaml
from pydantic import BaseModel
from utils.common import get_resource_path

def load_config_tools(yaml_path: str = "config/tools.yaml") -> dict:
    config_path = get_resource_path(yaml_path)
    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    tool_map = {}

    for tool in data["tools"]:
        tool_name = tool["name"]
        for func in tool["functions"]:
            func_name = func["name"]
            key = f"{tool_name}.{func_name}"

            module_path = func["module"]
            function_name = func["function"]

            schema_class = None
            param_names = []
            param_desc = {}
            response_fields = {}
            source = None

            if "schema_module" in func and "schema_class" in func:
                schema_module = importlib.import_module(func["schema_module"])
                schema_class = getattr(schema_module, func["schema_class"])

                if issubclass(schema_class, BaseModel):
                    for field_name, model_field in schema_class.model_fields.items():
                        param_names.append(field_name)
                        param_desc[field_name] = {
                            "type": str(model_field.annotation),
                            "description": model_field.description or ""
                        }
            if "response_schema_module" in func and "response_schema_class" in func:
                response_schema_module = importlib.import_module(func["response_schema_module"])
                response_schema_class = getattr(response_schema_module, func["response_schema_class"])

                if issubclass(response_schema_class, BaseModel):
                    for field_name, model_field in response_schema_class.model_fields.items():
                        response_fields[field_name] = {
                            "type": str(model_field.annotation),
                            "description": model_field.description or ""
                        }

            if "source" in func:
                source = func["source"]

            tool_map[key] = {
                "module": module_path,
                "function": function_name,
                "schema": schema_class,
                "param_names": param_names,
                "params": param_desc,
                "response_fields": response_fields,
                "source": source,
            }

    return tool_map