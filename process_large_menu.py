#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理大型菜单数据的工具
"""

import json
import sys
from json_to_excel import JsonToExcelConverter

def process_large_menu_data(input_file, output_file=None):
    """处理大型菜单数据"""
    
    print(f"🚀 开始处理大型菜单数据: {input_file}")
    print("=" * 60)
    
    try:
        # 读取JSON数据
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 数据类型: {type(data)}")
        
        if isinstance(data, list):
            print(f"📋 顶级菜单数量: {len(data)}")
            total_menus = 0
            
            # 统计每个顶级菜单的子菜单数量
            for i, menu in enumerate(data):
                if isinstance(menu, dict):
                    display_name = menu.get('resourcesDisplayName', f'菜单{i+1}')
                    child_count = len(menu.get('childResources', []))
                    total_menus += 1
                    print(f"📋 顶级菜单 {i+1}: {display_name} (子菜单数: {child_count})")
                    
                    # 递归统计子菜单
                    def count_children(children, level=1):
                        count = 0
                        for child in children:
                            count += 1
                            if child.get('childResources'):
                                count += count_children(child['childResources'], level + 1)
                        return count
                    
                    if child_count > 0:
                        total_children = count_children(menu['childResources'])
                        print(f"    └─ 总计子菜单: {total_children}")
                        total_menus += total_children
            
            print(f"\n📊 预估总菜单数: {total_menus}")
            
        elif isinstance(data, dict):
            print(f"📋 单个菜单对象: {data.get('resourcesDisplayName', '未知')}")
            # 如果是单个菜单对象，转换为数组格式
            data = [data]
        
        # 使用转换器处理数据
        converter = JsonToExcelConverter()
        
        if output_file:
            # 如果指定了输出文件，直接使用文件名
            excel_file = converter.convert_to_excel(json_data=json.dumps(data))
            if excel_file:
                # 重命名文件
                import os
                os.rename(excel_file, output_file)
                excel_file = output_file
        else:
            excel_file = converter.convert_to_excel(json_data=json.dumps(data))
        
        if excel_file:
            print(f"\n✅ 转换完成！")
            print(f"📄 Excel文件: {excel_file}")
            
            # 显示统计信息
            converter.print_menu_structure()
            
            return excel_file
        else:
            print("❌ 转换失败")
            return None
            
    except Exception as e:
        print(f"❌ 处理失败: {str(e)}")
        return None

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python process_large_menu.py <输入文件> [输出文件]")
        print("示例: python process_large_menu.py large_menu_data.json")
        print("示例: python process_large_menu.py large_menu_data.json output.xlsx")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    process_large_menu_data(input_file, output_file)

if __name__ == "__main__":
    main() 