# src/validation/validators.py

from typing import Dict, List, Any
import json
from pathlib import Path
import jsonschema

class TaskValidator:
    """Валидатор тестовых заданий."""
    
    TASK_SCHEMA = {
        "type": "object",
        "required": ["task_id", "type", "question"],
        "properties": {
            "task_id": {"type": "string"},
            "type": {"type": "string", "enum": ["MCQ", "FRQ", "CT", "RT"]},
            "question": {"type": "string"},
            "options": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 2
            },
            "correct": {"type": "string"},
            "explanation": {"type": "string"},
            "metadata": {
                "type": "object",
                "properties": {
                    "difficulty": {"type": "number", "minimum": 0, "maximum": 1},
                    "discriminative_power": {"type": "number", "minimum": 0, "maximum": 1},
                    "time_limit": {"type": "integer", "minimum": 0}
                }
            }
        }
    }
    
    def __init__(self, tasks_dir: str = "benchmarks"):
        self.tasks_dir = Path(tasks_dir)
    
    def validate_task(self, task: Dict) -> List[str]:
        """Проверяет одно задание на соответствие схеме."""
        errors = []
        try:
            jsonschema.validate(instance=task, schema=self.TASK_SCHEMA)
        except jsonschema.exceptions.ValidationError as e:
            errors.append(f"Schema validation error: {e.message}")
        
        # Дополнительные проверки
        if task["type"] == "MCQ" and not task.get("options"):
            errors.append("MCQ task must have options")
        if task["type"] == "MCQ" and not task.get("correct"):
            errors.append("MCQ task must have correct answer")
            
        return errors
    
    def validate_file(self, file_path: Path) -> List[str]:
        """Проверяет файл с заданиями."""
        errors = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tasks = json.load(f)
                
            if not isinstance(tasks, list):
                tasks = [tasks]
                
            for task in tasks:
                task_errors = self.validate_task(task)
                if task_errors:
                    errors.extend([f"Task {task.get('task_id', 'unknown')}: {e}" 
                                 for e in task_errors])
        except json.JSONDecodeError as e:
            errors.append(f"JSON parsing error in {file_path}: {str(e)}")
        except Exception as e:
            errors.append(f"Error processing {file_path}: {str(e)}")
            
        return errors
    
    def validate_all(self) -> Dict[str, List[str]]:
        """Проверяет все файлы с заданиями."""
        results = {}
        for category_dir in self.tasks_dir.iterdir():
            if category_dir.is_dir():
                for task_file in category_dir.glob("*.json"):
                    errors = self.validate_file(task_file)
                    if errors:
                        results[str(task_file)] = errors
        return results
