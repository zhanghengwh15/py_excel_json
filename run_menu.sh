#!/bin/bash

# Menu模块启动脚本
# 用于从根目录运行menu文件夹中的功能

echo "🚀 Menu模块启动脚本"
echo "=================="

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先创建虚拟环境"
    exit 1
fi

# 激活虚拟环境
source venv/bin/activate

# 进入menu目录
cd menu

echo "📁 当前工作目录: $(pwd)"
echo ""

# 显示可用选项
echo "请选择要运行的功能："
echo "1. 获取菜单详情 (menu_detail_fetcher.py)"
echo "2. 转换资源数据 (convert_to_id_map.py)"
echo "3. 导出用户角色权限 (user_role_permission_export.py)"
echo "4. 查看menu文件夹内容"
echo "5. 退出"
echo ""

read -p "请输入选项 (1-5): " choice

case $choice in
    1)
        echo "🔄 开始获取菜单详情..."
        python menu_detail_fetcher.py
        ;;
    2)
        echo "🔄 开始转换资源数据..."
        python convert_to_id_map.py
        ;;
    3)
        echo "🔄 开始导出用户角色权限..."
        python user_role_permission_export.py
        ;;
    4)
        echo "📋 menu文件夹内容："
        ls -la
        echo ""
        echo "📁 role文件夹内容："
        ls -la role/ | head -20
        ;;
    5)
        echo "👋 退出"
        exit 0
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "✅ 操作完成" 