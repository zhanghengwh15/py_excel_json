#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

# 读取JSON文件
with open('test_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"JSON数据类型: {type(data)}")

if isinstance(data, dict):
    print(f"JSON字典包含键: {list(data.keys())}")
    print(f"字典长度: {len(data)}")
    
    # 检查是否有数组类型的值
    for key, value in data.items():
        if isinstance(value, list):
            print(f"键 '{key}' 包含数组，长度: {len(value)}")
            if len(value) > 0 and isinstance(value[0], dict):
                print(f"  第一个元素包含键: {list(value[0].keys())}")
                print(f"  第一个元素的resourcesDisplayName: {value[0].get('resourcesDisplayName', '未找到')}")
elif isinstance(data, list):
    print(f"JSON数组包含 {len(data)} 个元素")
    if len(data) > 0 and isinstance(data[0], dict):
        print(f"第一个元素包含键: {list(data[0].keys())}")
        print(f"第一个元素的resourcesDisplayName: {data[0].get('resourcesDisplayName', '未找到')}")
else:
    print(f"JSON是其他类型: {data}") 