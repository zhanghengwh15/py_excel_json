#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查Excel文件内容
"""

import pandas as pd
import sys
import os

def check_excel_content(filename):
    """检查Excel文件内容"""
    try:
        df = pd.read_excel(filename)
        print(f"📊 Excel文件: {filename}")
        print(f"📋 总行数: {len(df)}")
        print(f"📋 列名: {list(df.columns)}")
        print("\n📋 前10行数据:")
        print(df.head(10))
        
        print("\n📋 菜单层级统计:")
        print(df['菜单层级'].value_counts().sort_index())
        
        print("\n📋 类型统计:")
        print(df['类型'].value_counts())
        
        # 检查顶级菜单
        top_level = df[df['菜单层级'] == 1]
        print(f"\n📋 顶级菜单 ({len(top_level)} 个):")
        for _, row in top_level.iterrows():
            print(f"  - {row['菜单名称']}")
            
    except Exception as e:
        print(f"❌ 读取Excel文件失败: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        # 查找最新的Excel文件
        import glob
        excel_files = glob.glob("*.xlsx")
        if excel_files:
            filename = max(excel_files, key=lambda x: os.path.getctime(x))
        else:
            print("❌ 未找到Excel文件")
            sys.exit(1)
    
    check_excel_content(filename) 