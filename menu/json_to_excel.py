#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 兼容性处理：如果python3不可用，尝试使用python
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
import requests
from typing import List, Dict, Any


class JsonToExcelConverter:
    """JSON转Excel转换器"""
    
    def __init__(self):
        self.menu_data = []
    
    def get_user_list(self, base_url: str = "https://cloudsy.shede.com.cn", 
                     headers: Dict[str, str] = None, 
                     request_data: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        获取用户列表（支持分页）
        
        Args:
            base_url: 基础URL
            headers: 请求头
            request_data: 请求数据
            
        Returns:
            List[Dict]: 用户列表，包含 nickName 和 userId
        """
        import time
        
        url = f"{base_url}/api/poit-cloud-platform/user/ent/user/page"
        
        # 默认请求头
        default_headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-cn',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json; charset=UTF-8',
            'Origin': base_url,
            'Pragma': 'no-cache',
            'Referer': f'{base_url}/cloud/cloud_config/userManagement',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'loglevel': 'debug',
            'menusUri': '/userManagement',
            'orgId': '1000879',
            'poit-cloud-org': '1d7d84a6f6b14d6d97f9c7a94813bb22',
            'poit-cloud-src-client': 'cloud',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'token': 'a7ab82cde0b64c45805d92fa65612c5f',
            'userId': '501073',
            'x-poit-tif-submit': '1675135120_1753070008803'
        }
        
        # 合并自定义请求头
        if headers:
            default_headers.update(headers)
        
        # 默认请求数据
        default_data = {
            "eid": "1d7d84a6f6b14d6d97f9c7a94813bb22",
            "operateUserId": "501073",
            "orgId": "1000879",
            "uid": "77c6e33e1b7d4371aecc6477322ff759",
            "appVersion": "1.0",
            "keyword": "",
            "combineStatus": None,
            "pageSize": 100,
            "pageNum": 1,
            "positionIdList": [],
            "roleIdList": [],
            "factoryIdList": [],
            "departmentIdList": []
        }
        
        # 合并自定义请求数据
        if request_data:
            default_data.update(request_data)
        
        all_users = []
        page_num = 1
        
        try:
            while True:
                # 更新页码
                default_data['pageNum'] = page_num
                
                print(f"📄 正在获取第 {page_num} 页用户数据...")
                
                response = requests.post(url, headers=default_headers, json=default_data)
                response.raise_for_status()
                
                result = response.json()
                
                # 检查响应数据
                if 'data' not in result:
                    print("❌ 响应数据格式不正确，缺少data字段")
                    break
                
                # 如果data为空，说明已经获取完所有数据
                if not result['data'] or len(result['data']) == 0:
                    print(f"✅ 已获取完所有用户数据，共 {len(all_users)} 个用户")
                    break
                
                # 提取用户数据
                if isinstance(result['data'], list):
                    page_users = []
                    for user in result['data']:
                        page_users.append({
                            'nickName': user.get('nickName', ''),
                            'userId': user.get('userId', ''),
                            'openUserId': user.get('openUserId', '') 
                        })
                    
                    all_users.extend(page_users)
                    print(f"   ✅ 第 {page_num} 页获取到 {len(page_users)} 个用户")
                    
                    # 如果当前页的用户数量小于pageSize，说明已经是最后一页
                    if len(page_users) < default_data['pageSize']:
                        print(f"✅ 已获取完所有用户数据，共 {len(all_users)} 个用户")
                        break
                else:
                    print("❌ 响应data字段不是数组格式")
                    break
                
                # 页码递增
                page_num += 1
                
                # 请求间隔200ms
                time.sleep(0.2)
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 获取用户列表失败: {str(e)}")
            return all_users  # 返回已获取的数据
        
        return all_users
    

    

    

    
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
    
    def convert_to_excel(self, json_file_path: str = None, json_data: str = None, 
                        filename_prefix: str = "") -> str:
        """
        将JSON转换为Excel文件
        
        Args:
            json_file_path: JSON文件路径
            json_data: JSON字符串数据
            filename_prefix: 文件名前缀
            
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
            data_to_use = self.menu_data
            sheet_name = '菜单结构'
            data_count = len(self.menu_data)
            
            # 创建DataFrame
            df = pd.DataFrame(data_to_use)
            
            # 生成文件名（yyyyMMddHHmm格式）
            timestamp = datetime.now().strftime('%Y%m%d%H%M')
            if filename_prefix:
                excel_filename = f"{filename_prefix}_{timestamp}.xlsx"
            else:
                excel_filename = f"{timestamp}.xlsx"
            
            # 保存为Excel文件并添加格式
            with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name=sheet_name)
                
                # 获取工作表
                worksheet = writer.sheets[sheet_name]
                
                # 设置列宽
                worksheet.column_dimensions['A'].width = 50  # 菜单名称
                worksheet.column_dimensions['B'].width = 10  # 菜单层级
                worksheet.column_dimensions['C'].width = 15  # 类型
                header_cols = ['A1', 'B1', 'C1']
                
                # 设置标题行格式
                from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
                
                # 标题行样式
                header_font = Font(bold=True, color="FFFFFF")
                header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
                header_alignment = Alignment(horizontal="center", vertical="center")
                
                # 应用标题行格式
                for col in header_cols:
                    cell = worksheet[col]
                    cell.font = header_font
                    cell.fill = header_fill
                    cell.alignment = header_alignment
                
                # 冻结标题行（第1行）
                worksheet.freeze_panes = 'A2'
                
                # 设置数据行格式
                data_alignment = Alignment(horizontal="left", vertical="center")
                center_alignment = Alignment(horizontal="center", vertical="center")
                
                # 为不同类型设置不同颜色
                menu_fill = PatternFill(start_color="E6F3FF", end_color="E6F3FF", fill_type="solid")
                function_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
                
                # 设置边框
                thin_border = Border(
                    left=Side(style='thin'),
                    right=Side(style='thin'),
                    top=Side(style='thin'),
                    bottom=Side(style='thin')
                )
                
                # 应用数据行格式
                for row in range(2, len(df) + 2):  # 从第2行开始（跳过标题行）
                    # 普通菜单数据格式
                    worksheet[f'A{row}'].alignment = data_alignment
                    worksheet[f'B{row}'].alignment = center_alignment
                    worksheet[f'C{row}'].alignment = center_alignment
                    
                    # 设置边框
                    for col in ['A', 'B', 'C']:
                        worksheet[f'{col}{row}'].border = thin_border
                    
                    # 根据类型设置背景色
                    type_cell = worksheet[f'C{row}']
                    if type_cell.value == "菜单":
                        type_cell.fill = menu_fill
                    elif type_cell.value == "功能":
                        type_cell.fill = function_fill
                

            
            print(f"✅ Excel文件已生成: {excel_filename}")
            print(f"📊 共处理 {data_count} 条数据")
            
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
    """主函数 - 用于JSON文件转Excel"""
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