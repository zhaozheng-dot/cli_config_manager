import json
import yaml
from pathlib import Path
from typing import List, Dict, Any, Tuple
from pydantic import ValidationError

# 导入定义的模型
from .models import User

class DataProcessor:
    """
    数据处理服务类。
    Java 类比: @Service public class UserDataService {...}
    """

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def load_raw_data(self) -> List[Any]:
        """
        读取 YAML 或 JSON 文件，返回原始的字典列表。
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        # 确保文件句柄自动关闭 (try-with-resources)
        with open(self.file_path, 'r', encoding='utf-8') as f:
            if self.file_path.suffix.lower() in ['.yaml', '.yml']:
                content = yaml.safe_load(f)
            elif self.file_path.suffix.lower() == '.json':
                content = json.load(f)
            else:
                raise ValueError("Unsupported file format. Use .yaml or .json")

        return content if isinstance(content, list) else []

    def process_data(self) -> Tuple[List[User], List[Dict[str, Any]]]:
        """
        核心业务逻辑：将原始数据转换为 User 对象，分离合法与非法数据。
        """
        raw_data = self.load_raw_data()
        valid_users: List[User] = []
        validation_errors: List[Dict[str, Any]] = []

        for index, entry in enumerate(raw_data):
            try:
                # 字典解包转换为 Pydantic 模型
                user = User(**entry)
                valid_users.append(user)
            except ValidationError as e:
                error_record = {
                    "index": index,
                    "raw_data": entry,
                    "errors": e.errors(include_url=False, include_context=False)
                }
                validation_errors.append(error_record)

        return valid_users, validation_errors

    def save_cleaned_data(self, users: List[User], output_path: Path):
        """
        将合法的 User 对象列表序列化为 JSON 文件。
        """
        # 使用列表推导式转换对象为 dict
        data_to_save = [user.model_dump(mode='json') for user in users]

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=2, ensure_ascii=False)