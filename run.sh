#!/bin/bash

# JSON转Excel工具启动脚本
# 使用方法: ./run.sh [json文件路径]

echo "🚀 JSON转Excel工具启动脚本"
echo "================================"

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖包..."
pip install -r requirements.txt

# 运行转换工具
echo "🔄 开始转换..."
if [ $# -eq 0 ]; then
    echo "📝 使用示例数据"
    python json_to_excel.py
else
    echo "📁 使用JSON文件: $1"
    python json_to_excel.py "$1"
fi

echo "✅ 脚本执行完成！" 