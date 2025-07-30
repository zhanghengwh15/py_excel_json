#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON文件合并工具
将两个JSON文件根据resourcesId和presourcesId的关系进行合并
"""

import json
import sys
from typing import Dict, List, Any

def load_json_file(file_path: str) -> List[Dict[str, Any]]:
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 不存在")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误：JSON文件 {file_path} 格式错误: {e}")
        sys.exit(1)

def build_resource_map(resources: List[Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
    """构建资源ID到资源对象的映射"""
    resource_map = {}
    
    def process_resource(resource):
        resource_id = resource.get('resourcesId')
        if resource_id:
            resource_map[resource_id] = resource
        
        # 递归处理子资源
        child_resources = resource.get('childResources', [])
        for child in child_resources:
            process_resource(child)
    
    for resource in resources:
        process_resource(resource)
    
    return resource_map

def sort_resources_by_sort(resources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """按sort字段对资源列表进行排序"""
    def sort_recursive(resource_list):
        # 对当前层级按sort排序
        sorted_list = sorted(resource_list, key=lambda x: x.get('sort', 0))
        
        # 递归对子资源排序
        for resource in sorted_list:
            child_resources = resource.get('childResources', [])
            if child_resources:
                resource['childResources'] = sort_recursive(child_resources)
        
        return sorted_list
    
    return sort_recursive(resources)

def merge_resources(app_resources: List[Dict[str, Any]], pc_resources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """合并两个资源列表"""
    # 构建资源映射
    app_resource_map = build_resource_map(app_resources)
    pc_resource_map = build_resource_map(pc_resources)
    
    # 合并资源映射
    merged_resource_map = {**app_resource_map, **pc_resource_map}
    
    # 重建树形结构
    def rebuild_tree(resources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        root_resources = []
        resource_map = {}
        
        # 首先创建所有资源的映射
        for resource in resources:
            resource_id = resource.get('resourcesId')
            if resource_id:
                resource_map[resource_id] = resource.copy()
                resource_map[resource_id]['childResources'] = []
        
        # 构建父子关系
        for resource in resources:
            resource_id = resource.get('resourcesId')
            parent_id = resource.get('presourcesId', 0)
            
            if parent_id == 0:
                # 根资源
                if resource_id in resource_map:
                    root_resources.append(resource_map[resource_id])
            else:
                # 子资源
                if parent_id in resource_map and resource_id in resource_map:
                    resource_map[parent_id]['childResources'].append(resource_map[resource_id])
        
        return root_resources
    
    # 合并所有资源
    all_resources = list(merged_resource_map.values())
    
    # 重建树形结构
    merged_tree = rebuild_tree(all_resources)
    
    # 按sort字段排序
    sorted_tree = sort_resources_by_sort(merged_tree)
    
    return sorted_tree

def save_json_file(data: List[Dict[str, Any]], file_path: str):
    """保存JSON文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"合并后的JSON文件已保存到: {file_path}")
    except Exception as e:
        print(f"错误：保存文件失败: {e}")
        sys.exit(1)

def main():
    """主函数"""
    print("开始合并JSON文件...")
    
    # 加载两个JSON文件
    print("加载 app.json...")
    app_data = load_json_file('app.json')
    
    print("加载 pc.json...")
    pc_data = load_json_file('pc.json')
    
    print(f"app.json 包含 {len(app_data)} 个根资源")
    print(f"pc.json 包含 {len(pc_data)} 个根资源")
    
    # 合并资源
    print("正在合并资源...")
    merged_data = merge_resources(app_data, pc_data)
    
    print(f"合并后包含 {len(merged_data)} 个根资源")
    
    # 保存合并后的文件
    output_file = 'merged_resources.json'
    save_json_file(merged_data, output_file)
    
    # 统计信息
    def count_resources(resources):
        count = 0
        for resource in resources:
            count += 1
            count += count_resources(resource.get('childResources', []))
        return count
    
    total_resources = count_resources(merged_data)
    print(f"合并完成！总共包含 {total_resources} 个资源节点")
    print("✓ 已按sort字段对同级资源进行排序")

if __name__ == "__main__":
    main() 