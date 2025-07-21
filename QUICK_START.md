# JSON转Excel工具 - 快速开始指南

## 🚀 环境配置

### 1. 创建虚拟环境（首次使用）
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 使用便捷启动脚本
```bash
# 给启动脚本添加执行权限（首次使用）
chmod +x run.sh

# 运行脚本
./run.sh user_menu_export.py
```

## 📋 使用方法

### 方法一：使用便捷启动脚本（推荐）
```bash
# 运行用户菜单权限导出
./run.sh user_menu_export.py

# 运行JSON转Excel工具
./run.sh json_to_excel.py

# 运行批量用户权限导出
./run.sh json_to_excel.py --batch-users
```

### 方法二：手动激活虚拟环境
```bash
# 激活虚拟环境
source venv/bin/activate

# 运行脚本
python user_menu_export.py
python json_to_excel.py
python json_to_excel.py --batch-users
```

## 🔧 配置说明

### 用户菜单权限导出配置
在 `user_menu_export.py` 中修改以下参数：
- `token`: 认证令牌
- `userId`: 当前操作用户ID
- `orgId`: 组织ID
- `eid`: 企业ID
- `uid`: 用户唯一标识
- `poit-cloud-org`: 云组织标识

### JSON转Excel配置
- 支持直接传入JSON文件路径
- 支持传入JSON字符串
- 支持批量用户权限导出

## 📊 输出文件

- 生成的Excel文件保存在项目根目录
- 文件名格式：`用户菜单权限_YYYYMMDDHHMM.xlsx`
- 包含用户名称、菜单路径、菜单层级、类型等信息

## ⚠️ 注意事项

1. **网络连接**：确保能访问目标API服务器
2. **认证信息**：使用前请更新配置文件中的认证参数
3. **请求频率**：脚本已内置请求间隔，避免过于频繁的API调用
4. **数据量**：大量用户数据导出可能需要较长时间

## 🛠️ 故障排除

### 问题：ModuleNotFoundError
```bash
# 解决方案：重新安装依赖
source venv/bin/activate
pip install -r requirements.txt
```

### 问题：权限错误
```bash
# 解决方案：添加执行权限
chmod +x run.sh
```

### 问题：网络连接失败
- 检查网络连接
- 验证API服务器地址
- 确认认证信息正确性 