import re
import sys
import uuid
import importlib.util
from pathlib import Path
from pydantic import BaseModel
from langchain.tools import BaseTool
from typing import List, Optional, Tuple

from src.app.database.vector_db import VectorDatabase, vector_db
from src.app.genai.tools.static_tools import tools as static_tools

PATH_TOOLS = Path("src/app/genai/tools/generated/")


class ToolMetadata(BaseModel):
    tool_id: str
    tool_name: str
    description: str
    module_path: Path


class ToolManager:
    def __init__(self, vector_db: VectorDatabase):
        self.vector_db = vector_db
        self.tools: List[Tuple[str, BaseTool]] = []
        self.vector_db.reset_vector_db()
        # self._load_static_tools()
        self._load_existing_tools()


    def _load_existing_tools(self):
        if not PATH_TOOLS.exists():
            return
        
        for py_file in PATH_TOOLS.glob("*.py"):
            tool_name = py_file.stem
            print(tool_name)
            try:
                tool_function = self.import_tool_function(py_file, tool_name)
                if tool_function:
                    tool_metadata = self.register_tool_in_db(tool_function)
                    self.tools.append((tool_metadata.tool_id, tool_function))
                else:
                    raise ValueError(f"Skipped invalid tool: {tool_name}")
            except Exception as e:
                raise ValueError(f"Error loading {tool_name}: {e}")


    def  _load_static_tools(self):
        for tool in static_tools:
            try:
                tool_metadata = self.register_tool_in_db(tool)
                self.tools.append((tool_metadata.tool_id, tool))
            except Exception as e:
                raise ValueError(f"Error loading static tool: {e}")


    def _extract_tool_name(self, tool_code: str) -> Optional[str]:
        function_match = re.search(r'def\s+(\w+)\s*\(', tool_code)
        return function_match.group(1) if function_match else None


    def save_tool_to_file(self, tool_name: str, tool_code: str) -> Path:
        PATH_TOOLS.mkdir(exist_ok=True, parents=True)
        module_path = PATH_TOOLS / f"{tool_name.lower()}.py"
        module_path.write_text(tool_code, encoding="utf-8")
        return module_path
    

    def import_tool_function(self, module_path: Path, tool_name: str) -> Optional[BaseTool]:
        try:
            module_name = module_path.stem
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            tool_function: BaseTool = getattr(module, tool_name, None)
            return tool_function if callable(tool_function) else None
        
        except Exception as e:
            raise ValueError(f"Failed to import tool function: {e}")

    def register_tool_in_db(self, tool_function: BaseTool) -> ToolMetadata:
        tool_specs = tool_function.args_schema.model_json_schema()
        tool_id = str(uuid.uuid4())
        self.vector_db.insert_vector(
            tool_descr=tool_specs["description"],
            tool_id=tool_id
        )
        metadata = ToolMetadata(
            tool_id=tool_id,
            tool_name=tool_function.name,
            description=tool_specs["description"],
            module_path=PATH_TOOLS / f"{tool_function.name.lower()}.py"
        )
        return metadata
    

    def generate_and_register_tool(self, tool_code: str) -> Tuple[ToolMetadata, BaseTool]:
        tool_name = self._extract_tool_name(tool_code)
        if not tool_name:
            raise ValueError("Tool function name extraction failed.")

        try:
            compiled_code = compile(tool_code, tool_name, "exec")
            exec(compiled_code, {})
        except Exception as e:
            raise ValueError(f"Compilation/execution error: {e}")

        module_path = self.save_tool_to_file(tool_name, tool_code)
        tool_function = self.import_tool_function(module_path, tool_name)

        if tool_function is None:
            raise ValueError("Failed to import the tool function from generated code.")

        metadata = self.register_tool_in_db(tool_function)
        self.tools.append((metadata.tool_id, tool_function))
        
        return metadata, tool_function
    

    def get_tools_by_ids(self, tool_ids: List[str]) -> List[BaseTool]:
        return [
            tool for tid in tool_ids
            for stored_id, tool in self.tools if tid == stored_id
        ]
    

    def delete_tool(self, tool_id: str) -> bool:
        try:
            self.vector_db.delete_vector(tool_id=tool_id)
            self.tools = [(tid, tool) for tid, tool in self.tools if tid != tool_id]
            return True
        except Exception:
            return False


    def update_tool(self, tool_id: str, updated_tool_code: str) -> ToolMetadata:
        # Delete old tool
        if not self.delete_tool(tool_id):
            raise ValueError("Failed to delete existing tool.")

        # Generate & register new tool
        return self.generate_and_register_tool(updated_tool_code)
    

    def find_best_tool(self, query: str, top_k: int = 3) -> List[str]:
        result = self.vector_db.query_vector(query)
        if result and result["ids"]:
            return result["ids"][0][:top_k]
        return []
    

tool_manager = ToolManager(vector_db)
