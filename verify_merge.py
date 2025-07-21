#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证合并结果的脚本
"""

import json

def load_json_file(file_path):
    """加载JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def count_resources(resources):
    """统计资源数量"""
    count = 0
    for resource in resources:
        count += 1
        count += count_resources(resource.get('childResources', []))
    return count

def get_resource_ids(resources):
    """获取所有资源ID"""
    resource_ids = set()
    
    def collect_ids(resource_list):
        for resource in resource_list:
            resource_id = resource.get('resourcesId')
            if resource_id:
                resource_ids.add(resource_id)
            collect_ids(resource.get('childResources', []))
    
    collect_ids(resources)
    return resource_ids

def main():
    print("验证合并结果...")
    
    # 加载原始文件
    app_data = load_json_file('app.json')
    pc_data = load_json_file('pc.json')
    merged_data = load_json_file('merged_resources.json')
    
    # 统计资源数量
    app_count = count_resources(app_data)
    pc_count = count_resources(pc_data)
    merged_count = count_resources(merged_data)
    
    print(f"app.json 资源数量: {app_count}")
    print(f"pc.json 资源数量: {pc_count}")
    print(f"merged_resources.json 资源数量: {merged_count}")
    
    # 获取资源ID集合
    app_ids = get_resource_ids(app_data)
    pc_ids = get_resource_ids(pc_data)
    merged_ids = get_resource_ids(merged_data)
    
    print(f"app.json 唯一资源ID数量: {len(app_ids)}")
    print(f"pc.json 唯一资源ID数量: {len(pc_ids)}")
    print(f"merged_resources.json 唯一资源ID数量: {len(merged_ids)}")
    
    # 检查是否有重复
    intersection = app_ids & pc_ids
    if intersection:
        print(f"发现重复的资源ID: {len(intersection)} 个")
        print(f"重复的ID示例: {list(intersection)[:5]}")
    else:
        print("没有发现重复的资源ID")
    
    # 检查合并是否完整
    expected_ids = app_ids | pc_ids
    if merged_ids == expected_ids:
        print("✓ 合并结果正确：所有资源都已包含")
    else:
        missing = expected_ids - merged_ids
        extra = merged_ids - expected_ids
        if missing:
            print(f"✗ 缺少资源ID: {missing}")
        if extra:
            print(f"✗ 多余资源ID: {extra}")
    
    # 检查根资源数量
    print(f"app.json 根资源数量: {len(app_data)}")
    print(f"pc.json 根资源数量: {len(pc_data)}")
    print(f"merged_resources.json 根资源数量: {len(merged_data)}")
    
    # 检查appType分布
    app_types = {}
    def collect_app_types(resources):
        for resource in resources:
            app_type = resource.get('appType')
            if app_type:
                app_types[app_type] = app_types.get(app_type, 0) + 1
            collect_app_types(resource.get('childResources', []))
    
    collect_app_types(merged_data)
    print(f"appType分布: {app_types}")

if __name__ == "__main__":
    main() 