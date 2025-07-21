#!/bin/bash

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 激活虚拟环境
source "$SCRIPT_DIR/venv/bin/activate"

# 检查是否提供了参数
if [ $# -eq 0 ]; then
    echo "使用方法:"
    echo "  ./run.sh json_to_excel.py [参数...]"
    echo "  ./run.sh user_menu_export.py [参数...]"
    echo ""
    echo "示例:"
    echo "  ./run.sh json_to_excel.py"
    echo "  ./run.sh json_to_excel.py --batch-users"
    echo "  ./run.sh user_menu_export.py"
    exit 1
fi

# 运行Python脚本
python "$@" 