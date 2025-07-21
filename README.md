# JSON转Excel工具

这是一个用于将JSON格式的菜单数据转换为Excel格式的Python工具。

## 功能特性

- 🔄 解析JSON格式的菜单数据
- 📊 转换为Excel格式，包含菜单名称、菜单层级和类型三列
- 🌳 支持多层级菜单结构，显示完整路径
- 🏷️ 自动识别菜单类型（菜单/功能）
- 🎨 Excel格式美化：标题加粗居中，不同类型用颜色区分
- 📅 自动生成时间戳格式的文件名（yyyyMMddHHmm）
- 🎯 保持原始菜单顺序不变

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 方法一：使用示例数据（推荐用于测试）

```bash
python json_to_excel.py
```

### 方法二：使用自定义JSON文件

```bash
python json_to_excel.py your_data.json
```

### 方法三：在Python代码中使用

```python
from json_to_excel import JsonToExcelConverter

# 创建转换器实例
converter = JsonToExcelConverter()

# 方式1：使用JSON文件
excel_file = converter.convert_to_excel(json_file_path="menu_data.json")

# 方式2：使用JSON字符串
json_data = '''
[
    {
        "resourcesDisplayName": "系统管理",
        "childResources": [
            {
                "resourcesDisplayName": "用户管理",
                "childResources": []
            }
        ]
    }
]
'''
excel_file = converter.convert_to_excel(json_data=json_data)
```

## JSON数据格式

工具期望的JSON数据格式如下：

```json
[
    {
        "resourcesDisplayName": "菜单显示名称",
        "childResources": [
            {
                "resourcesDisplayName": "子菜单显示名称",
                "childResources": []
            }
        ]
    }
]
```

### 字段说明

- `resourcesDisplayName`: 菜单的显示名称（必填）
- `childResources`: 子菜单列表（可选，如果为空数组则表示没有子菜单）

## 输出格式

生成的Excel文件包含以下列：

| 列名 | 说明 | 示例 |
|------|------|------|
| 菜单名称 | 菜单的完整路径名称 | "计划排产 - 基础配置 - 生产提前期" |
| 菜单层级 | 菜单在层级结构中的深度 | 1, 2, 3... |
| 类型 | 菜单类型 | "菜单" 或 "功能" |

### 菜单名称规则

- **第一层级**: 直接显示 `resourcesDisplayName`
- **第二层级及以下**: 显示格式为 `"完整父级路径 - 当前菜单名称"`

### 类型识别规则

- **resourcesType = 1**: 显示为 "菜单"
- **resourcesType = 2**: 显示为 "功能"

### Excel格式美化

- **标题行**: 蓝色背景，白色加粗字体，居中对齐
- **菜单类型**: 浅蓝色背景
- **功能类型**: 浅黄色背景
- **列宽**: 自动调整以适应内容

### 文件命名规则

Excel文件名格式：`yyyyMMddHHmm.xlsx`

例如：`202412011430.xlsx` 表示2024年12月1日14点30分生成的文件

## 示例输出

### 输入JSON
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

## 注意事项

1. **编码格式**: JSON文件必须使用UTF-8编码
2. **数据完整性**: 确保JSON数据格式正确，包含必要的字段
3. **文件权限**: 确保程序有权限在项目根目录创建Excel文件
4. **依赖版本**: 建议使用Python 3.7或更高版本

## 错误处理

工具会处理以下常见错误：

- JSON格式错误
- 文件不存在或无法读取
- 缺少必要字段
- 文件写入权限问题

## 开发说明

### 项目结构
```
py_excel/
├── json_to_excel.py    # 主程序文件
├── requirements.txt    # 依赖包列表
├── README.md          # 说明文档
└── *.xlsx             # 生成的Excel文件
```

### 核心类

- `JsonToExcelConverter`: 主要的转换器类
  - `parse_json_data()`: 递归解析JSON数据
  - `convert_to_excel()`: 转换为Excel文件
  - `print_menu_structure()`: 打印菜单结构预览

## 许可证

本项目采用MIT许可证。 