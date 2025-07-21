# 🚀 快速使用指南

## 一键运行（推荐）

### 方法一：使用启动脚本
```bash
# 使用示例数据
./run.sh

# 使用自定义JSON文件
./run.sh your_data.json
```

### 方法二：手动运行
```bash
# 1. 激活虚拟环境
source venv/bin/activate

# 2. 运行工具
python json_to_excel.py                    # 使用示例数据
python json_to_excel.py your_data.json     # 使用自定义文件
```

## 📋 功能说明

✅ **已实现功能**：
- 解析JSON格式的菜单数据
- 提取 `resourcesDisplayName` 作为菜单名称
- 递归处理 `childResources` 子菜单
- 生成Excel文件，包含"菜单名称"、"菜单层级"和"类型"三列
- 菜单名称格式：显示完整路径（如："计划排产 - 基础配置 - 生产提前期"）
- 类型识别：resourcesType=1显示为"菜单"，resourcesType=2显示为"功能"
- Excel格式美化：标题加粗居中，不同类型用颜色区分
- 文件名格式：`yyyyMMddHHmm.xlsx`（如：202412011430.xlsx）
- 保持原始菜单顺序不变

## 📊 输出示例

### 输入JSON结构
```json
[
    {
        "resourcesDisplayName": "系统管理",
        "childResources": [
            {
                "resourcesDisplayName": "用户管理",
                "childResources": [
                    {
                        "resourcesDisplayName": "用户列表",
                        "childResources": []
                    }
                ]
            }
        ]
    }
]
```

### 输出Excel内容
| 菜单名称 | 菜单层级 | 类型 |
|----------|----------|------|
| 计划排产 | 1 | 菜单 |
| 计划排产 - 基础配置 | 2 | 菜单 |
| 计划排产 - 基础配置 - 生产提前期 | 3 | 菜单 |
| 计划排产 - 基础配置 - 窖池初始化 - 查询 | 4 | 功能 |

## 🔧 自定义使用

### 在Python代码中使用
```python
from json_to_excel import JsonToExcelConverter

converter = JsonToExcelConverter()

# 使用JSON文件
excel_file = converter.convert_to_excel(json_file_path="menu_data.json")

# 使用JSON字符串
json_data = '[...]'
excel_file = converter.convert_to_excel(json_data=json_data)
```

## 📁 项目文件说明

- `json_to_excel.py` - 主程序文件
- `sample_menu_data.json` - 示例JSON数据
- `requirements.txt` - Python依赖包
- `run.sh` - 一键启动脚本
- `README.md` - 详细说明文档
- `venv/` - Python虚拟环境
- `*.xlsx` - 生成的Excel文件

## ⚠️ 注意事项

1. **JSON格式要求**：
   - 必须包含 `resourcesDisplayName` 字段
   - 子菜单通过 `childResources` 数组表示
   - 文件编码必须是UTF-8

2. **运行环境**：
   - Python 3.7+
   - 需要安装pandas和openpyxl包

3. **文件权限**：
   - 确保有权限在项目根目录创建Excel文件

## 🆘 常见问题

**Q: 提示"command not found: pip"**
A: 使用 `pip3` 或创建虚拟环境后使用 `pip`

**Q: 提示"externally-managed-environment"**
A: 使用提供的 `run.sh` 脚本，它会自动创建虚拟环境

**Q: Excel文件没有生成**
A: 检查JSON格式是否正确，确保包含必要的字段

**Q: 中文显示乱码**
A: 确保JSON文件使用UTF-8编码保存 