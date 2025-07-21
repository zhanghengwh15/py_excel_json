#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API功能测试脚本
用于测试用户列表获取和菜单权限获取功能
"""

import time
from json_to_excel import JsonToExcelConverter


def test_user_list_api():
    """测试用户列表API"""
    print("🧪 测试用户列表API...")
    
    converter = JsonToExcelConverter()
    
    # 模拟请求数据（需要根据实际情况修改）
    test_headers = {
        'token': 'test_token',
        'userId': 'test_user_id',
        'orgId': 'test_org_id',
    }
    
    test_request_data = {
        "eid": "test_eid",
        "operateUserId": "test_operate_user_id",
        "orgId": "test_org_id",
        "uid": "test_uid",
        "pageSize": 10,  # 小页面用于测试
    }
    
    try:
        # 测试获取用户列表（会显示分页和间隔信息）
        users = converter.get_user_list(
            headers=test_headers,
            request_data=test_request_data
        )
        
        print(f"✅ 用户列表API测试完成，获取到 {len(users)} 个用户")
        return True
        
    except Exception as e:
        print(f"❌ 用户列表API测试失败: {str(e)}")
        return False


def test_menu_permissions_api():
    """测试菜单权限API"""
    print("🧪 测试菜单权限API...")
    
    converter = JsonToExcelConverter()
    
    # 模拟请求数据（需要根据实际情况修改）
    test_headers = {
        'token': 'test_token',
        'userId': 'test_user_id',
        'orgId': 'test_org_id',
    }
    
    test_request_data = {
        "eid": "test_eid",
        "orgId": "test_org_id",
        "uid": "test_uid",
    }
    
    try:
        # 测试获取菜单权限（会显示300ms间隔）
        menu_data = converter.get_user_menu_permissions(
            user_id="test_user_id",
            headers=test_headers,
            request_data=test_request_data
        )
        
        print(f"✅ 菜单权限API测试完成，获取到 {len(menu_data) if menu_data else 0} 条菜单数据")
        return True
        
    except Exception as e:
        print(f"❌ 菜单权限API测试失败: {str(e)}")
        return False


def test_time_intervals():
    """测试时间间隔功能"""
    print("⏱️ 测试时间间隔功能...")
    
    start_time = time.time()
    
    # 模拟200ms间隔
    time.sleep(0.2)
    interval1 = time.time() - start_time
    
    # 模拟300ms间隔
    time.sleep(0.3)
    interval2 = time.time() - start_time
    
    print(f"✅ 200ms间隔测试: {interval1:.3f}s")
    print(f"✅ 300ms间隔测试: {interval2:.3f}s")
    
    return True


def main():
    """主测试函数"""
    print("🚀 API功能测试开始")
    print("=" * 50)
    
    # 测试时间间隔
    test_time_intervals()
    print()
    
    # 测试用户列表API（会失败，因为使用了测试数据）
    print("⚠️  注意：以下API测试会失败，因为使用了测试数据")
    print("   请在实际使用时配置正确的参数")
    print()
    
    test_user_list_api()
    print()
    
    test_menu_permissions_api()
    print()
    
    print("🎉 测试完成！")
    print("💡 提示：要成功测试API，请在 user_menu_export.py 中配置正确的参数")


if __name__ == "__main__":
    main() 