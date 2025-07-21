#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON转Excel工具
功能：解析JSON数据，提取菜单信息并转换为Excel格式
作者：AI Assistant
日期：2024
"""

import json
import pandas as pd
from datetime import datetime
import os
import sys
from typing import List, Dict, Any


class JsonToExcelConverter:
    """JSON转Excel转换器"""
    
    def __init__(self):
        self.menu_data = []
    
    def parse_json_data(self, json_data: List[Dict[str, Any]], parent_path: str = "", level: int = 1) -> None:
        """
        递归解析JSON数据，提取菜单信息
        
        Args:
            json_data: JSON数据列表
            parent_path: 父级菜单路径
            level: 当前层级
        """
        for item in json_data:
            # 获取显示名称和类型
            display_name = item.get('resourcesDisplayName', '')
            resources_type = item.get('resourcesType', 1)
            
            # 构建菜单全路径
            if parent_path:
                menu_path = f"{parent_path} - {display_name}"
            else:
                menu_path = display_name
            
            # 确定类型显示
            type_display = "菜单" if resources_type == 1 else "功能"
            
            # 添加到数据列表
            self.menu_data.append({
                '菜单名称': menu_path,
                '菜单层级': level,
                '类型': type_display
            })
            
            # 递归处理子菜单
            child_resources = item.get('childResources', [])
            if child_resources:
                self.parse_json_data(child_resources, menu_path, level + 1)
    
    def process_json_data(self, data: Any) -> None:
        """
        处理JSON数据，支持多种格式
        
        Args:
            data: JSON数据
        """
        if isinstance(data, list):
            # 如果数据是数组，每个元素都是第一层级的菜单
            self.parse_json_data(data)
        elif isinstance(data, dict):
            # 如果数据是字典，尝试找到包含菜单数据的字段
            if 'data' in data:
                if isinstance(data['data'], list):
                    self.parse_json_data(data['data'])
                else:
                    self.parse_json_data([data['data']])
            elif 'resources' in data:
                if isinstance(data['resources'], list):
                    self.parse_json_data(data['resources'])
                else:
                    self.parse_json_data([data['resources']])
            elif 'childResources' in data:
                # 如果数据本身就是一个菜单对象，直接处理
                self.parse_json_data([data])
            else:
                # 假设数据本身就是菜单
                self.parse_json_data([data])
        else:
            raise ValueError(f"不支持的JSON数据类型: {type(data)}")
    
    def convert_to_excel(self, json_file_path: str = None, json_data: str = None) -> str:
        """
        将JSON转换为Excel文件
        
        Args:
            json_file_path: JSON文件路径
            json_data: JSON字符串数据
            
        Returns:
            str: 生成的Excel文件路径
        """
        try:
            # 解析JSON数据
            if json_file_path:
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            elif json_data:
                data = json.loads(json_data)
            else:
                raise ValueError("必须提供JSON文件路径或JSON字符串数据")
            
            # 清空之前的数据
            self.menu_data = []
            
            # 解析数据
            self.process_json_data(data)
            
            # 创建DataFrame
            df = pd.DataFrame(self.menu_data)
            
            # 生成文件名（yyyyMMddHHmm格式）
            timestamp = datetime.now().strftime('%Y%m%d%H%M')
            excel_filename = f"{timestamp}.xlsx"
            
            # 保存为Excel文件并添加格式
            with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='菜单结构')
                
                # 获取工作表
                worksheet = writer.sheets['菜单结构']
                
                # 设置列宽
                worksheet.column_dimensions['A'].width = 50  # 菜单名称
                worksheet.column_dimensions['B'].width = 10  # 菜单层级
                worksheet.column_dimensions['C'].width = 15  # 类型
                
                # 设置标题行格式
                from openpyxl.styles import Font, Alignment, PatternFill
                
                # 标题行样式
                header_font = Font(bold=True, color="FFFFFF")
                header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                header_alignment = Alignment(horizontal="center", vertical="center")
                
                # 应用标题行格式
                for col in ['A1', 'B1', 'C1']:
                    cell = worksheet[col]
                    cell.font = header_font
                    cell.fill = header_fill
                    cell.alignment = header_alignment
                
                # 冻结标题行（第1行）
                worksheet.freeze_panes = 'A2'
                
                # 设置数据行格式
                data_alignment = Alignment(horizontal="left", vertical="center")
                
                # 为不同类型设置不同颜色
                menu_fill = PatternFill(start_color="E6F3FF", end_color="E6F3FF", fill_type="solid")
                function_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
                
                # 应用数据行格式
                for row in range(2, len(df) + 2):  # 从第2行开始（跳过标题行）
                    # 设置对齐方式
                    worksheet[f'A{row}'].alignment = data_alignment
                    worksheet[f'B{row}'].alignment = Alignment(horizontal="center", vertical="center")
                    worksheet[f'C{row}'].alignment = Alignment(horizontal="center", vertical="center")
                    
                    # 根据类型设置背景色
                    type_cell = worksheet[f'C{row}']
                    if type_cell.value == "菜单":
                        type_cell.fill = menu_fill
                    elif type_cell.value == "功能":
                        type_cell.fill = function_fill
            
            print(f"✅ Excel文件已生成: {excel_filename}")
            print(f"📊 共处理 {len(self.menu_data)} 条菜单数据")
            
            return excel_filename
            
        except Exception as e:
            print(f"❌ 转换失败: {str(e)}")
            return None
    
    def print_menu_structure(self, max_items: int = 50) -> None:
        """打印菜单结构（用于调试）"""
        print(f"\n📋 菜单结构预览 (显示前{max_items}项):")
        print("-" * 80)
        
        # 只显示前max_items项，避免输出过多
        display_items = self.menu_data[:max_items]
        for item in display_items:
            indent = "  " * (item['菜单层级'] - 1)
            type_icon = "📁" if item['类型'] == "菜单" else "⚙️"
            print(f"{indent}├─ {type_icon} {item['菜单名称']} (层级: {item['菜单层级']}, 类型: {item['类型']})")
        
        if len(self.menu_data) > max_items:
            print(f"    ... 还有 {len(self.menu_data) - max_items} 项菜单")
        
        # 显示统计信息
        print(f"\n📊 菜单统计:")
        print(f"   总菜单数: {len(self.menu_data)}")
        
        # 按层级统计
        level_counts = {}
        for item in self.menu_data:
            level = item['菜单层级']
            level_counts[level] = level_counts.get(level, 0) + 1
        
        for level in sorted(level_counts.keys()):
            print(f"   第{level}级: {level_counts[level]} 项")
        
        # 按类型统计
        type_counts = {}
        for item in self.menu_data:
            menu_type = item['类型']
            type_counts[menu_type] = type_counts.get(menu_type, 0) + 1
        
        for menu_type, count in type_counts.items():
            print(f"   {menu_type}: {count} 项")


def main():
    """主函数"""
    converter = JsonToExcelConverter()
    
    print("🚀 JSON转Excel工具")
    print("=" * 50)
    
    # 示例JSON数据（用于测试）
    sample_json = '''
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
                        },
                        {
                            "resourcesDisplayName": "角色管理",
                            "childResources": []
                        }
                    ]
                },
                {
                    "resourcesDisplayName": "权限管理",
                    "childResources": [
                        {
                            "resourcesDisplayName": "菜单权限",
                            "childResources": []
                        }
                    ]
                }
            ]
        },
        {
            "resourcesDisplayName": "业务管理",
            "childResources": [
                {
                    "resourcesDisplayName": "订单管理",
                    "childResources": []
                }
            ]
        }
    ]
    '''
    
    # 检查是否有命令行参数
    if len(sys.argv) > 1:
        json_file_path = sys.argv[1]
        print(f"📁 使用JSON文件: {json_file_path}")
        excel_file = converter.convert_to_excel(json_file_path=json_file_path)
    else:
        print("📝 使用示例数据")
        excel_file = converter.convert_to_excel(json_data=sample_json)
    
    if excel_file:
        # 显示菜单结构预览
        converter.print_menu_structure()
        
        print(f"\n📄 Excel文件已保存到项目根目录: {excel_file}")
        print("🎉 转换完成！")


if __name__ == "__main__":
    main() 