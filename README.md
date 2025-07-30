# JSON转Excel工具

这是一个功能强大的Python工具集，包含两个主要功能：
1. **JSON菜单数据转Excel**：将JSON格式的菜单数据转换为Excel格式
2. **用户菜单权限批量导出**：通过API批量获取用户列表和对应的菜单权限，导出到Excel

## 功能特性

### 基础功能
- 🔄 解析JSON格式的菜单数据
- 📊 转换为Excel格式，包含菜单名称、菜单层级和类型列
- 🌳 支持多层级菜单结构，显示完整路径
- 🏷️ 自动识别菜单类型（菜单/功能）
- 🎨 Excel格式美化：标题加粗居中，不同类型用颜色区分
- 📅 自动生成时间戳格式的文件名（yyyyMMddHHmm）
- 🎯 保持原始菜单顺序不变

### 新增：用户菜单权限批量导出功能
- 🚀 批量获取用户列表（通过API调用，支持分页）
- 👥 批量获取每个用户的菜单权限详情
- 📋 合并用户信息和菜单权限，导出到Excel
- 🔗 相同用户的单元格自动合并
- 📊 详细的统计信息显示
- ⚙️ 支持自定义API配置
- ⏱️ 智能请求间隔（用户列表200ms，菜单权限300ms），确保API稳定性
- 📄 自动分页处理，支持大量用户数据

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 功能一：JSON菜单数据转Excel

#### 方法一：使用示例数据（推荐用于测试）

```bash
python json_to_excel.py
```

#### 方法二：使用自定义JSON文件

```bash
python json_to_excel.py your_data.json
```

#### 方法三：在Python代码中使用

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

### 功能二：用户菜单权限批量导出

#### 方法一：使用独立脚本（推荐）

```bash
# 直接运行批量导出
python user_menu_export.py

# 查看配置模板
python user_menu_export.py --template
```

#### 方法二：使用主程序的批量模式

```bash
python json_to_excel.py --batch-users
```

#### 方法三：在Python代码中使用

```python
from json_to_excel import JsonToExcelConverter

# 创建转换器实例
converter = JsonToExcelConverter()

# 配置API请求参数
custom_headers = {
    'token': 'your_token_here',
    'userId': 'your_user_id_here',
    'orgId': 'your_org_id_here',
    'poit-cloud-org': 'your_cloud_org_here'
}

user_request_data = {
    "eid": "your_enterprise_id_here",
    "operateUserId": "your_operate_user_id_here",
    "orgId": "your_org_id_here",
    "uid": "your_uid_here",
    "pageSize": 100
}

menu_request_data = {
    "eid": "your_enterprise_id_here",
    "orgId": "your_org_id_here",
    "uid": "your_uid_here"
}

# 批量处理用户菜单权限
success = converter.batch_process_user_permissions(
    headers=custom_headers,
    user_request_data=user_request_data,
    menu_request_data=menu_request_data
)

if success:
    # 导出到Excel
    excel_file = converter.convert_to_excel(
        use_user_data=True, 
        filename_prefix="用户菜单权限"
    )
```

#### 配置说明

在使用用户菜单权限批量导出功能前，需要在 `user_menu_export.py` 文件中配置以下参数：

1. **token**: API认证令牌（必填）
2. **userId**: 当前操作用户ID（必填）
3. **orgId**: 组织ID（必填）
4. **eid**: 企业ID（必填）
5. **uid**: 用户唯一标识（必填）
6. **poit-cloud-org**: 云组织标识（必填）

这些参数可以从浏览器的开发者工具中获取，具体步骤：
1. 在浏览器中登录系统
2. 打开开发者工具（F12）
3. 切换到Network选项卡
4. 执行一次用户管理相关的操作
5. 查看请求头中的相关参数

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

### JSON菜单转Excel输出格式

生成的Excel文件包含以下列：

| 列名 | 说明 | 示例 |
|------|------|------|
| 菜单名称 | 菜单的完整路径名称 | "计划排产 - 基础配置 - 生产提前期" |
| 菜单层级 | 菜单在层级结构中的深度 | 1, 2, 3... |
| 类型 | 菜单类型 | "菜单" 或 "功能" |

### 用户菜单权限导出格式

生成的Excel文件包含以下列：

| 列名 | 说明 | 示例 |
|------|------|------|
| 用户名称 | 用户的显示名称（nickName） | "张三" |
| 菜单名称 | 菜单的完整路径名称 | "计划排产 - 基础配置 - 生产提前期" |
| 菜单层级 | 菜单在层级结构中的深度 | 1, 2, 3... |
| 类型 | 菜单类型 | "菜单" 或 "功能" |

**特殊格式说明：**
- 相同用户的多个菜单权限行，用户名称列会自动合并成一个单元格
- 便于快速查看每个用户拥有的所有菜单权限

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

### JSON菜单转Excel示例

#### 输入JSON
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

#### 输出Excel内容
| 菜单名称 | 菜单层级 | 类型 |
|----------|----------|------|
| 系统管理 | 1 | 菜单 |
| 系统管理 - 用户管理 | 2 | 菜单 |
| 系统管理 - 用户管理 - 用户列表 | 3 | 菜单 |

### 用户菜单权限导出示例

#### 输出Excel内容（带用户名称）
| 用户名称 | 菜单名称 | 菜单层级 | 类型 |
|----------|----------|----------|------|
| 张三 | 系统管理 | 1 | 菜单 |
| 张三 | 系统管理 - 用户管理 | 2 | 菜单 |
| 张三 | 系统管理 - 用户管理 - 用户列表 | 3 | 菜单 |
| 张三 | 系统管理 - 用户管理 - 用户添加 | 3 | 功能 |
| 李四 | 系统管理 | 1 | 菜单 |
| 李四 | 系统管理 - 权限管理 | 2 | 菜单 |
| 李四 | 系统管理 - 权限管理 - 角色管理 | 3 | 菜单 |

**注意：在实际Excel文件中，相同用户名称（如"张三"、"李四"）的单元格会被合并**

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
├── json_to_excel.py      # 主程序文件（JSON转Excel + 用户权限批量导出）
├── user_menu_export.py   # 用户菜单权限批量导出专用脚本
├── test_api.py          # API功能测试脚本
├── requirements.txt      # 依赖包列表
├── README.md            # 说明文档
├── QUICK_START.md       # 快速开始指南
└── *.xlsx               # 生成的Excel文件
```

### 核心类

- `JsonToExcelConverter`: 主要的转换器类
  
  **基础功能方法：**
  - `parse_json_data()`: 递归解析JSON数据
  - `convert_to_excel()`: 转换为Excel文件（支持普通菜单和用户权限数据）
  - `print_menu_structure()`: 打印菜单结构预览
  
  **用户权限批量处理方法：**
  - `get_user_list()`: 获取用户列表（通过API）
  - `get_user_menu_permissions()`: 获取指定用户的菜单权限（通过API）
  - `parse_user_menu_data()`: 解析用户菜单数据
  - `batch_process_user_permissions()`: 批量处理用户菜单权限
  - `_merge_user_cells()`: 合并相同用户的Excel单元格

## 许可证

本项目采用MIT许可证。 