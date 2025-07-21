#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试JSON数据结构
"""

import json

def debug_json_structure(filename):
    """调试JSON数据结构"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 JSON文件: {filename}")
        print(f"📋 数据类型: {type(data)}")
        
        if isinstance(data, dict):
            print(f"📋 字典键: {list(data.keys())}")
            
            # 检查是否有childResources字段
            if 'childResources' in data:
                child_resources = data['childResources']
                print(f"📋 childResources类型: {type(child_resources)}")
                if isinstance(child_resources, list):
                    print(f"📋 childResources数组长度: {len(child_resources)}")
                    print(f"📋 顶级菜单: {data.get('resourcesDisplayName', '未知')}")
                    
                    # 检查每个子菜单
                    for i, item in enumerate(child_resources):
                        if isinstance(item, dict):
                            display_name = item.get('resourcesDisplayName', '未知')
                            resources_type = item.get('resourcesType', '未知')
                            child_count = len(item.get('childResources', []))
                            print(f"📋 子菜单[{i}]: {display_name} (类型: {resources_type}, 子菜单数: {child_count})")
                            
                            # 只显示前5个，避免输出过多
                            if i >= 4:
                                print(f"📋 ... 还有 {len(child_resources) - 5} 个子菜单")
                                break
                else:
                    print(f"📋 childResources不是数组: {child_resources}")
            
            # 检查是否有data字段
            elif 'data' in data:
                print(f"📋 data字段类型: {type(data['data'])}")
                if isinstance(data['data'], list):
                    print(f"📋 data数组长度: {len(data['data'])}")
                    for i, item in enumerate(data['data'][:3]):
                        if isinstance(item, dict):
                            display_name = item.get('resourcesDisplayName', '未知')
                            print(f"📋 data[{i}]: {display_name}")
                else:
                    print(f"📋 data不是数组: {data['data']}")
            
            # 检查是否有resources字段
            elif 'resources' in data:
                print(f"📋 resources字段类型: {type(data['resources'])}")
                if isinstance(data['resources'], list):
                    print(f"📋 resources数组长度: {len(data['resources'])}")
                    for i, item in enumerate(data['resources'][:3]):
                        if isinstance(item, dict):
                            display_name = item.get('resourcesDisplayName', '未知')
                            print(f"📋 resources[{i}]: {display_name}")
                else:
                    print(f"📋 resources不是数组: {data['resources']}")
            
            # 检查其他可能的字段
            else:
                print(f"📋 字典内容预览:")
                for key, value in list(data.items())[:5]:
                    print(f"📋 {key}: {type(value)} - {str(value)[:100]}...")
                    
        elif isinstance(data, list):
            print(f"📋 数组长度: {len(data)}")
            print(f"📋 前3个元素类型: {[type(item) for item in data[:3]]}")
            
            # 检查每个顶级菜单
            for i, item in enumerate(data):
                if isinstance(item, dict):
                    display_name = item.get('resourcesDisplayName', '未知')
                    resources_type = item.get('resourcesType', '未知')
                    child_count = len(item.get('childResources', []))
                    print(f"📋 第{i+1}个顶级菜单: {display_name} (类型: {resources_type}, 子菜单数: {child_count})")
                    
                    # 只显示前3个，避免输出过多
                    if i >= 2:
                        print(f"📋 ... 还有 {len(data) - 3} 个顶级菜单")
                        break
        else:
            print(f"📋 数据不是数组或字典，而是: {type(data)}")
            
    except Exception as e:
        print(f"❌ 读取JSON文件失败: {str(e)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "test_data.json"
    debug_json_structure(filename) 