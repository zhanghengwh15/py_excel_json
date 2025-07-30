# Menu 模块

这个文件夹包含了所有与菜单权限相关的代码和数据文件。

## 文件结构

### 核心脚本
- `user_role_permission_export.py` - 用户角色权限导出主脚本
- `menu_detail_fetcher.py` - 菜单详情获取脚本
- `convert_to_id_map.py` - 将嵌套JSON转换为扁平化ID映射
- `json_to_excel.py` - 通用JSON转Excel工具
- `merge_json.py` - JSON文件合并工具
- `user_menu_export.py` - 用户菜单导出工具
- `check_excel.py` - Excel文件检查工具

### 数据文件
- `merged_resources.json` - 原始嵌套资源数据
- `id_map.json` - 扁平化的资源ID映射
- `app.json` - 应用配置数据
- `pc.json` - PC端配置数据

### 角色权限数据
- `role/` - 角色权限文件夹
  - `3000xxxx.json` - 各个角色的权限ID列表

### 输出文件
- `用户角色权限_YYYYMMDDHHMM.xlsx` - 导出的Excel文件

## 使用方法

### 1. 获取菜单详情
```bash
python menu_detail_fetcher.py
```

### 2. 转换资源数据
```bash
python convert_to_id_map.py
```

### 3. 导出用户角色权限
```bash
python user_role_permission_export.py
```

## 数据流程

1. **获取角色列表** → `menu_detail_fetcher.py`
2. **获取角色权限** → 生成 `role/*.json` 文件
3. **转换资源数据** → `merged_resources.json` → `id_map.json`
4. **导出用户权限** → 最终Excel文件

## 注意事项

- 所有脚本都需要在虚拟环境中运行
- 确保网络连接正常，能够访问API
- 导出的Excel文件会包含：用户名称、菜单名称、菜单层级、资源类型 