#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证合并后的JSON文件是否按sort字段正确排序
"""

import json

def load_json_file(file_path):
    """加载JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def check_sort_order(resources, level=0):
    """检查排序是否正确"""
    if not resources:
        return True
    
    # 检查当前层级的sort值是否递增
    sort_values = [resource.get('sort', 0) for resource in resources]
    is_sorted = sort_values == sorted(sort_values)
    
    if not is_sorted:
        print(f"  {'  ' * level}✗ 第{level}层级排序错误:")
        for i, resource in enumerate(resources):
            print(f"  {'  ' * level}    {i+1}. {resource.get('resourcesName', 'Unknown')} (sort: {resource.get('sort', 0)})")
        return False
    
    # 递归检查子资源
    all_children_sorted = True
    for resource in resources:
        child_resources = resource.get('childResources', [])
        if child_resources:
            if not check_sort_order(child_resources, level + 1):
                all_children_sorted = False
    
    return all_children_sorted

def show_sort_info(resources, level=0):
    """显示排序信息"""
    for i, resource in enumerate(resources):
        name = resource.get('resourcesName', 'Unknown')
        sort_val = resource.get('sort', 0)
        print(f"{'  ' * level}{i+1}. {name} (sort: {sort_val})")
        
        child_resources = resource.get('childResources', [])
        if child_resources:
            show_sort_info(child_resources, level + 1)

def main():
    print("验证合并后的JSON文件排序...")
    
    # 加载合并后的文件
    merged_data = load_json_file('merged_resources.json')
    
    print(f"根资源数量: {len(merged_data)}")
    print("\n根资源排序情况:")
    show_sort_info(merged_data[:5])  # 只显示前5个根资源
    
    # 检查排序是否正确
    print("\n检查排序正确性...")
    if check_sort_order(merged_data):
        print("✓ 所有层级的排序都是正确的")
    else:
        print("✗ 发现排序错误")
    
    # 统计sort值分布
    sort_values = []
    def collect_sort_values(resources):
        for resource in resources:
            sort_values.append(resource.get('sort', 0))
            collect_sort_values(resource.get('childResources', []))
    
    collect_sort_values(merged_data)
    
    print(f"\n排序统计:")
    print(f"  总资源数: {len(sort_values)}")
    print(f"  最小sort值: {min(sort_values)}")
    print(f"  最大sort值: {max(sort_values)}")
    print(f"  平均sort值: {sum(sort_values) / len(sort_values):.2f}")

if __name__ == "__main__":
    main() 