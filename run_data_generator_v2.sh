#!/bin/bash

# 酒鬼窖池历史数据生成器 V2 启动脚本
# 功能：根据Excel模板格式生成酒鬼窖池历史数据
# 作者：AI Assistant
# 日期：2024

echo "🍷 酒鬼窖池历史数据生成器 V2"
echo "================================"
echo "📋 功能说明："
echo "   - 窖池ID: 100-110（共11个窖池）"
echo "   - 窖池编码: 直接使用数字格式（100、101、102等）"
echo "   - 轮次格式: 2025-1"
echo "   - 日期格式: 2023/11/11"
echo "   - 时间范围: 1990-2025年"
echo "   - 只有3个sheet，每个sheet 100,000条记录"
echo "   - 总计: 3个sheet，300,000条记录"
echo "   - Sheet1: 投料耗用"
echo "   - Sheet2: 等级酒生产记录"
echo "   - Sheet3: 入窖出窖糟化验记录"
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先创建虚拟环境"
    exit 1
fi

# 激活虚拟环境并运行数据生成器
echo "🚀 启动数据生成器 V2..."
source venv/bin/activate && python data/generate_wine_cellar_data_v2.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 数据生成完成！"
    echo "📁 生成的文件在 data/ 目录下"
    echo "📊 包含以下数据类型："
    echo "   - 投料耗用（100,000条记录）"
    echo "   - 等级酒生产记录（100,000条记录）"
    echo "   - 入窖出窖糟化验记录（100,000条记录）"
    echo "📈 总计: 300,000条记录"
else
    echo "❌ 数据生成失败！"
    exit 1
fi 