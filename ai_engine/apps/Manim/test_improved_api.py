#!/usr/bin/env python3
"""
测试改进后的AI API - 验证语法问题是否修复
"""

import requests
import time

API_BASE = "http://localhost:8888"

def test_improved_generation():
    """测试改进后的视频生成"""
    
    # 测试用例 - 包含之前容易出错的内容
    test_cases = [
        {"text": "牛顿第一定律", "title": "物理基础"},
        {"text": "圆周运动", "title": "运动学"},
        {"text": "三角函数sin和cos", "title": "数学函数"},
        {"text": "极限的定义", "title": "微积分"},
        {"text": "热力学第二定律", "title": "热力学"}
    ]
    
    print("🧪 测试改进后的AI API")
    print("=" * 50)
    
    successful_generations = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 测试 {i}/{total_tests}: {test_case['text']}")
        
        try:
            start_time = time.time()
            
            response = requests.post(
                f"{API_BASE}/generate",
                json=test_case,
                timeout=120  # 2分钟超时
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print(f"✅ 生成成功 ({duration:.1f}秒)")
                    print(f"   🆔 视频ID: {data['video_id']}")
                    print(f"   📁 文件大小: {data['video_size']}")
                    print(f"   🎭 场景名: {data.get('scene_name', 'Unknown')}")
                    successful_generations += 1
                else:
                    print(f"❌ 生成失败: {data.get('error', '未知错误')}")
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print("⏰ 请求超时")
        except Exception as e:
            print(f"❌ 异常: {e}")
        
        # 短暂休息避免过载
        if i < total_tests:
            print("   ⏸️  等待3秒...")
            time.sleep(3)
    
    # 总结
    print("\n" + "=" * 50)
    print(f"🎉 测试完成！")
    print(f"✅ 成功率: {successful_generations}/{total_tests} ({successful_generations/total_tests*100:.1f}%)")
    
    if successful_generations == total_tests:
        print("🎊 完美！所有测试都通过了")
    elif successful_generations > total_tests * 0.8:
        print("👍 很好！大部分测试通过")
    else:
        print("⚠️  需要进一步优化")
    
    return successful_generations, total_tests

def test_api_features():
    """测试API的其他功能"""
    print("\n🔍 测试API其他功能")
    print("-" * 30)
    
    try:
        # 测试状态
        response = requests.get(f"{API_BASE}/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API状态: {data['ai_generator']}")
            print(f"   🤖 可用模型: {len(data.get('models', []))} 个")
        
        # 测试视频列表
        response = requests.get(f"{API_BASE}/videos")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 视频列表: {data['total']} 个视频")
            
            if data['videos']:
                latest = data['videos'][0]
                print(f"   📽️ 最新视频: {latest['input_text'][:15]}... ({latest['file_size']})")
        
    except Exception as e:
        print(f"❌ 功能测试失败: {e}")

if __name__ == "__main__":
    print("🚀 AI Manim API 改进效果测试")
    print("测试目标：验证语法错误修复情况")
    print()
    
    # 测试连接
    try:
        response = requests.get(f"{API_BASE}/", timeout=5)
        if response.status_code == 200:
            print("✅ API连接正常")
        else:
            print("❌ API连接失败")
            exit(1)
    except:
        print("❌ 无法连接到API，请确认服务器已启动")
        exit(1)
    
    # 主要测试
    successful, total = test_improved_generation()
    
    # 功能测试
    test_api_features()
    
    # 最终评估
    print(f"\n🎯 最终评估:")
    if successful == total:
        print("🎉 API改进非常成功！语法问题已完全解决")
    else:
        print(f"⚠️  还需要进一步优化 ({successful}/{total} 成功)") 