#!/bin/bash

# 酒鬼窖池历史数据生成脚本
# 作者：AI Assistant
# 日期：2024

echo "🍷 酒鬼窖池历史数据生成器"
echo "================================"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 检查依赖包
echo "📦 检查依赖包..."
python3 -c "import pandas, openpyxl" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 安装依赖包..."
    pip3 install pandas openpyxl
fi

# 运行数据生成器
echo "🚀 开始生成数据..."
python3 generate_wine_cellar_data.py

if [ $? -eq 0 ]; then
    echo "✅ 数据生成完成！"
    echo "📁 生成的文件在 data/ 目录下"
else
    echo "❌ 数据生成失败！"
    exit 1
fi 