#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将merged_resources.json转换为单层级的id_map.json
生成包含完整路径的资源映射
"""

import json
import os
from typing import List, Dict, Any

class ResourceConverter:
    def __init__(self):
        """初始化转换器"""
        self.id_map = []
        
    def build_path(self, resource: Dict[str, Any], parent_path: str = "") -> str:
        """
        构建资源的完整路径
        
        Args:
            resource: 资源对象
            parent_path: 父级路径
            
        Returns:
            完整的资源路径
        """
        current_name = resource.get('resourcesName', '')
        
        if parent_path:
            return f"{parent_path}/{current_name}"
        else:
            return current_name
    
    def process_resource(self, resource: Dict[str, Any], parent_path: str = "", level: int = 1):
        """
        递归处理单个资源及其子资源
        
        Args:
            resource: 资源对象
            parent_path: 父级路径
            level: 当前层级（从1开始）
        """
        # 构建当前资源的完整路径
        current_path = self.build_path(resource, parent_path)
        
        # 创建映射条目
        mapping_entry = {
            "path": current_path,
            "resourcesId": resource.get('resourcesId'),
            "resourcesType": resource.get('resourcesType'),
            "level": level,
            "sort": resource.get('sort', 0)
        }
        
        # 添加到映射列表
        self.id_map.append(mapping_entry)
        
        # 递归处理子资源
        child_resources = resource.get('childResources', [])
        for child in child_resources:
            self.process_resource(child, current_path, level + 1)
    
    def convert(self, input_file: str, output_file: str):
        """
        转换资源文件
        
        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径
        """
        print(f"开始转换 {input_file}...")
        
        try:
            # 读取输入文件
            with open(input_file, 'r', encoding='utf-8') as f:
                resources = json.load(f)
            
            print(f"读取到 {len(resources)} 个顶级资源")
            
            # 处理所有顶级资源
            for resource in resources:
                self.process_resource(resource)
            
            print(f"总共处理了 {len(self.id_map)} 个资源")
            
            # 保存输出文件
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.id_map, f, ensure_ascii=False, indent=2)
            
            print(f"转换完成！结果已保存到 {output_file}")
            
            # 显示一些示例
            print("\n示例数据:")
            for i, item in enumerate(self.id_map[:5]):
                print(f"  {i+1}. {item}")
            
            if len(self.id_map) > 5:
                print(f"  ... 还有 {len(self.id_map) - 5} 条数据")
                
        except FileNotFoundError:
            print(f"错误：找不到文件 {input_file}")
        except json.JSONDecodeError as e:
            print(f"错误：JSON解析失败 - {e}")
        except Exception as e:
            print(f"错误：{e}")


def main():
    """主函数"""
    input_file = "merged_resources.json"
    output_file = "id_map.json"
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"错误：找不到输入文件 {input_file}")
        return
    
    # 创建转换器并执行转换
    converter = ResourceConverter()
    converter.convert(input_file, output_file)


if __name__ == "__main__":
    main() 