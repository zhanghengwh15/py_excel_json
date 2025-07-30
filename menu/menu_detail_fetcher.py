#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
菜单ID详情获取脚本
获取角色列表并下载每个角色的详细资源信息
"""

import json
import os
import time
import requests
from typing import List, Dict, Any

class MenuDetailFetcher:
    def __init__(self):
        """初始化请求头和基础配置"""
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-cn',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json; charset=UTF-8',
            'Origin': 'https://cloudsy.shede.com.cn',
            'Pragma': 'no-cache',
            'Referer': 'https://cloudsy.shede.com.cn/cloud/cloud_config/roleManagement',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'loglevel': 'debug',
            'menusUri': '/roleManagement',
            'orgId': '1000879',
            'poit-cloud-org': '1d7d84a6f6b14d6d97f9c7a94813bb22',
            'poit-cloud-src-client': 'cloud',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'token': 'a7ab82cde0b64c45805d92fa65612c5f',
            'userId': '501073',
            'x-poit-tif-submit': '6147143675_1753085509575'
        }
        
        # Cookie 设置
        self.session.cookies.update({
            '_ga': 'GA1.3.690594394.1744712683',
            '_ga_F0DQ6TTSVW': 'GS2.3.s1752628062$o8$g1$t1752628198$j60$l0$h0'
        })
        
        # API URLs
        self.role_list_url = 'https://cloudsy.shede.com.cn/api/poit-cloud-platform/role/ent/list'
        self.role_detail_url = 'https://cloudsy.shede.com.cn/api/poit-cloud-platform/role/resourcesIds/list'
        
        # 创建输出目录
        self.output_dir = 'role'
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"创建输出目录: {self.output_dir}")

    def get_role_list(self) -> List[Dict[str, Any]]:
        """
        分页获取角色列表
        
        Returns:
            角色列表，包含roleId和appCode
        """
        all_roles = []
        page_num = 1
        page_size = 100
        
        while True:
            print(f"正在获取第 {page_num} 页角色列表...")
            
            # 构建请求数据
            data = {
                "eid": "1d7d84a6f6b14d6d97f9c7a94813bb22",
                "operateUserId": "501073",
                "orgId": "1000879",
                "uid": "77c6e33e1b7d4371aecc6477322ff759",
                "appVersion": "1.0",
                "pageNum": page_num,
                "pageSize": page_size,
                "roleName": "",
                "appCode": None
            }
            
            try:
                response = self.session.post(
                    self.role_list_url,
                    headers=self.headers,
                    json=data,
                    timeout=30
                )
                response.raise_for_status()
                
                result = response.json()
                
                # 检查响应状态
                if result.get('success') is False:
                    print(f"API返回错误: {result.get('message', '未知错误')}")
                    break
                
                # 获取角色数据 - roles数组在顶级对象中
                roles = result.get('roles', [])
                
                if not roles:
                    print(f"第 {page_num} 页没有更多角色数据，停止分页")
                    break
                
                print(f"第 {page_num} 页获取到 {len(roles)} 个角色")
                all_roles.extend(roles)
                
                page_num += 1
                
                # 分页间隔200ms
                time.sleep(0.2)
                
            except requests.exceptions.RequestException as e:
                print(f"请求第 {page_num} 页时发生错误: {e}")
                break
            except json.JSONDecodeError as e:
                print(f"解析第 {page_num} 页响应JSON时发生错误: {e}")
                break
        
        print(f"总共获取到 {len(all_roles)} 个角色")
        return all_roles

    def get_role_detail(self, role_id: str, app_code: str) -> Dict[str, Any]:
        """
        获取角色详细资源信息
        
        Args:
            role_id: 角色ID
            app_code: 应用代码
            
        Returns:
            角色详细信息
        """
        print(f"正在获取角色 {role_id} (appCode: {app_code}) 的详细信息...")
        
        # 构建请求数据
        data = {
            "eid": "1d7d84a6f6b14d6d97f9c7a94813bb22",
            "operateUserId": "501073",
            "orgId": "1000879",
            "uid": "77c6e33e1b7d4371aecc6477322ff759",
            "appVersion": "1.0",
            "appCode": app_code,
            "roleId": role_id
        }
        
        try:
            # 更新请求头中的submit时间戳
            current_time = str(int(time.time() * 1000))
            self.headers['x-poit-tif-submit'] = f"2041495486_{current_time}"
            
            response = self.session.post(
                self.role_detail_url,
                headers=self.headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            
            # 检查响应状态
            if result.get('success') is False:
                print(f"获取角色 {role_id} 详细信息失败: {result.get('message', '未知错误')}")
                return {}
            
            return result.get('data', {})
            
        except requests.exceptions.RequestException as e:
            print(f"请求角色 {role_id} 详细信息时发生错误: {e}")
            return {}
        except json.JSONDecodeError as e:
            print(f"解析角色 {role_id} 响应JSON时发生错误: {e}")
            return {}

    def save_role_detail(self, role_id: str, detail_data: Dict[str, Any]) -> bool:
        """
        保存角色详细信息到JSON文件
        
        Args:
            role_id: 角色ID
            detail_data: 详细信息数据
            
        Returns:
            是否保存成功
        """
        if not detail_data:
            print(f"角色 {role_id} 没有详细信息，跳过保存")
            return False
        
        file_path = os.path.join(self.output_dir, f"{role_id}.json")
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(detail_data, f, ensure_ascii=False, indent=2)
            
            print(f"角色 {role_id} 详细信息已保存到: {file_path}")
            return True
            
        except Exception as e:
            print(f"保存角色 {role_id} 详细信息时发生错误: {e}")
            return False

    def run(self):
        """执行完整的获取流程"""
        print("开始获取菜单ID详情...")
        print("=" * 50)
        
        # 第一步：获取角色列表
        roles = self.get_role_list()
        
        if not roles:
            print("未获取到任何角色信息，程序结束")
            return
        
        print("=" * 50)
        
        # 第二步：获取每个角色的详细信息
        success_count = 0
        fail_count = 0
        
        for i, role in enumerate(roles):
            role_id = role.get('roleId')
            app_code = role.get('appCode')
            
            if not role_id:
                print(f"第 {i+1} 个角色缺少roleId，跳过")
                fail_count += 1
                continue
            
            # 获取详细信息
            detail_data = self.get_role_detail(role_id, app_code)
            
            # 保存到文件
            if self.save_role_detail(role_id, detail_data):
                success_count += 1
            else:
                fail_count += 1
            
            # 请求间隔
            time.sleep(0.1)
        
        print("=" * 50)
        print(f"处理完成! 成功: {success_count}, 失败: {fail_count}")
        print(f"详细信息文件保存在: {os.path.abspath(self.output_dir)} 目录下")


def main():
    """主函数"""
    try:
        fetcher = MenuDetailFetcher()
        fetcher.run()
    except KeyboardInterrupt:
        print("\n用户中断程序")
    except Exception as e:
        print(f"程序执行过程中发生错误: {e}")


if __name__ == "__main__":
    main() 