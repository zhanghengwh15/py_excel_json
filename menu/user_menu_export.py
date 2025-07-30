#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户菜单权限批量导出工具
功能：批量获取用户列表和对应的菜单权限，导出到Excel文件
作者：AI Assistant
日期：2024
"""

import sys
import json
from json_to_excel import JsonToExcelConverter


def main():
    """批量导出用户菜单权限的主函数"""
    converter = JsonToExcelConverter()
    
    print("🚀 用户菜单权限批量导出工具")
    print("=" * 50)
    
    # 配置说明
    print("📋 配置说明：")
    print("   请在下面的配置中修改实际的参数值：")
    print("   - token: 认证令牌（必填）")
    print("   - userId: 当前操作用户ID（必填）")
    print("   - orgId: 组织ID（必填）")
    print("   - eid: 企业ID（必填）")
    print("   - uid: 用户唯一标识（必填）")
    print("   - poit-cloud-org: 云组织标识（必填）")
    print()
    print("📄 分页和间隔说明：")
    print("   - 用户列表采用分页获取，pageNum从1开始")
    print("   - 当返回的data为空时，表示已获取完所有数据")
    print("   - 用户列表请求间隔200ms，避免请求过于频繁")
    print("   - 菜单权限请求间隔300ms，确保API稳定性")
    print()
    
    # ===== 配置区域 - 请根据实际情况修改 =====
    
    # 基础URL（一般不需要修改）
    base_url = "https://cloudsy.shede.com.cn"
    
    # 请求头配置
    custom_headers = {
        'token': 'a7ab82cde0b64c45805d92fa65612c5f',  # ⚠️ 请替换为实际的token
        'userId': '501073',  # ⚠️ 请替换为实际的用户ID
        'orgId': '1000879',  # ⚠️ 请替换为实际的组织ID
        'poit-cloud-org': '1d7d84a6f6b14d6d97f9c7a94813bb22',  # ⚠️ 请替换为实际值
        'x-poit-tif-submit': '1675135120_1753070008803',  # 可选，可以根据实际情况修改
    }
    
    # 用户列表请求配置
    user_request_data = {
        "eid": "1d7d84a6f6b14d6d97f9c7a94813bb22",  # ⚠️ 请替换为实际的企业ID
        "operateUserId": "501073",  # ⚠️ 请替换为实际的操作用户ID
        "orgId": "1000879",  # ⚠️ 请替换为实际的组织ID
        "uid": "77c6e33e1b7d4371aecc6477322ff759",  # ⚠️ 请替换为实际的用户唯一标识
        "appVersion": "1.0",
        "keyword": "",  # 搜索关键词，可以为空
        "combineStatus": None,
        "pageSize": 100,  # 每页获取的用户数量，可以根据需要调整
        "pageNum": 1,  # 页码，从1开始
        "positionIdList": [],
        "roleIdList": [],
        "factoryIdList": [],
        "departmentIdList": []
    }
    
    # 菜单权限请求配置
    menu_request_data = {
        "eid": "1d7d84a6f6b14d6d97f9c7a94813bb22",  # ⚠️ 请替换为实际的企业ID
        "orgId": "1000879",  # ⚠️ 请替换为实际的组织ID
        "uid": "77c6e33e1b7d4371aecc6477322ff759",  # ⚠️ 请替换为实际的用户唯一标识
        "appVersion": "1.0"
    }
    
    # ===== 配置区域结束 =====
    
    print("📤 开始批量导出...")
    print()
    
    try:
        # 批量处理用户菜单权限
        success = converter.batch_process_user_permissions(
            headers=custom_headers,
            user_request_data=user_request_data,
            menu_request_data=menu_request_data
        )
        
        if success:
            # 导出到Excel
            excel_file = converter.convert_to_excel(
                use_user_data=True, 
                filename_prefix="用户菜单权限"
            )
            
            if excel_file:
                print(f"\n📄 Excel文件已保存到: {excel_file}")
                print("🎉 批量导出完成！")
                
                # 显示详细统计信息
                if converter.user_menu_data:
                    user_count = len(set(item['用户名称'] for item in converter.user_menu_data))
                    menu_count = len([item for item in converter.user_menu_data if item['类型'] == '菜单'])
                    function_count = len([item for item in converter.user_menu_data if item['类型'] == '功能'])
                    
                    print(f"\n📊 导出统计:")
                    print(f"   👥 用户总数: {user_count}")
                    print(f"   📋 菜单权限总数: {len(converter.user_menu_data)}")
                    print(f"   📁 菜单数量: {menu_count}")
                    print(f"   ⚙️  功能数量: {function_count}")
                    
                    print(f"\n💡 提示:")
                    print(f"   - Excel中相同用户的行已自动合并")
                    print(f"   - 菜单和功能用不同颜色区分")
                    print(f"   - 可以使用Excel的筛选功能查看特定用户的权限")
            else:
                print("❌ Excel文件生成失败")
        else:
            print("❌ 批量处理失败，请检查配置参数")
            
    except Exception as e:
        print(f"❌ 处理过程中发生错误: {str(e)}")
        print("\n🔧 故障排除提示:")
        print("   1. 检查网络连接是否正常")
        print("   2. 检查token是否有效且未过期")
        print("   3. 检查所有配置参数是否正确")
        print("   4. 检查用户是否有访问权限")


def print_configuration_template():
    """打印配置模板"""
    print("📝 配置模板:")
    print("=" * 50)
    
    template = {
        "custom_headers": {
            "token": "your_token_here",
            "userId": "your_user_id_here",
            "orgId": "your_org_id_here",
            "poit-cloud-org": "your_cloud_org_here"
        },
        "user_request_data": {
            "eid": "your_enterprise_id_here",
            "operateUserId": "your_operate_user_id_here",
            "orgId": "your_org_id_here",
            "uid": "your_uid_here",
            "pageSize": 100
        },
        "menu_request_data": {
            "eid": "your_enterprise_id_here",
            "orgId": "your_org_id_here",
            "uid": "your_uid_here"
        }
    }
    
    print(json.dumps(template, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--template":
        print_configuration_template()
    else:
        main() 