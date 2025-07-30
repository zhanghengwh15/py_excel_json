#!/bin/bash

# 酒鬼窖池历史数据生成器启动脚本
# 作者：AI Assistant
# 日期：2024

echo "🍷 酒鬼窖池历史数据生成器"
echo "================================"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先创建虚拟环境"
    exit 1
fi

# 激活虚拟环境并运行数据生成器
echo "🚀 启动数据生成器..."
source venv/bin/activate && python data/generate_wine_cellar_data.py

if [ $? -eq 0 ]; then
    echo "✅ 数据生成完成！"
    echo "📁 生成的文件在 data/ 目录下"
else
    echo "❌ 数据生成失败！"
    exit 1
fi 