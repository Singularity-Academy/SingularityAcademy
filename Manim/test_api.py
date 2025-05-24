#!/usr/bin/env python3
"""
AI Manim 视频生成器 API 测试客户端
"""

import requests
import json
import time

API_BASE = "http://localhost:7777"

def test_api_status():
    """测试API状态"""
    print("🔍 测试API状态...")
    try:
        response = requests.get(f"{API_BASE}/status")
        if response.status_code == 200:
            data = response.json()
            print("✅ API在线")
            print(f"   AI生成器状态: {data['ai_generator']}")
            print(f"   时间戳: {data['timestamp']}")
            return True
        else:
            print(f"❌ API状态异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API，请确认服务器已启动")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_generate_video(content, title=None):
    """测试视频生成"""
    print(f"\n🎬 测试视频生成: '{content}'")
    
    payload = {"content": content}
    if title:
        payload["title"] = title
    
    try:
        print("📤 发送请求...")
        response = requests.post(
            f"{API_BASE}/generate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"📥 响应状态: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ 视频生成成功!")
                print(f"   视频名称: {data['video_name']}")
                print(f"   视频ID: {data['video_id']}")
                print(f"   下载链接: {API_BASE}{data['video_url']}")
                print(f"   视频大小: {data['video_size']}")
                print(f"   场景类名: {data['scene_name']}")
                return data['video_id']
            else:
                print("⚠️ 视频生成失败")
                print(f"   消息: {data.get('message', '未知错误')}")
                return None
        else:
            print(f"❌ 请求失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None

def test_download_video(video_id):
    """测试视频下载"""
    print(f"\n📥 测试视频下载: {video_id}")
    
    try:
        response = requests.get(f"{API_BASE}/video/{video_id}")
        
        if response.status_code == 200:
            filename = f"downloaded_{video_id}.mp4"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ 视频下载成功: {filename}")
            print(f"   文件大小: {len(response.content)/1024:.1f} KB")
            return True
        else:
            print(f"❌ 下载失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 下载异常: {e}")
        return False

def test_list_videos():
    """测试视频列表"""
    print(f"\n📋 测试视频列表...")
    
    try:
        response = requests.get(f"{API_BASE}/videos")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取视频列表成功")
            print(f"   总计: {data['total']} 个视频")
            
            for video in data['videos'][:3]:  # 显示前3个
                print(f"   - {video['video_id']}: {video['size']} ({video['created_at'][:19]})")
            
            return data['videos']
        else:
            print(f"❌ 获取列表失败: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return []

def run_complete_test():
    """运行完整测试"""
    print("🧪 AI Manim 视频生成器 API 完整测试")
    print("=" * 50)
    
    # 1. 测试API状态
    if not test_api_status():
        print("\n❌ API不可用，停止测试")
        return
    
    # 2. 测试视频生成
    test_cases = [
        ("牛顿第一定律", "物理课程"),
        ("圆周运动", None),
        ("三角函数图像", "数学课程")
    ]
    
    generated_videos = []
    
    for content, title in test_cases:
        video_id = test_generate_video(content, title)
        if video_id:
            generated_videos.append(video_id)
            time.sleep(2)  # 避免请求过于频繁
    
    # 3. 测试视频列表
    videos = test_list_videos()
    
    # 4. 测试视频下载
    if generated_videos:
        test_download_video(generated_videos[0])
    
    print("\n" + "=" * 50)
    print("🎉 API测试完成!")
    print(f"✅ 成功生成 {len(generated_videos)} 个视频")
    print(f"📋 服务器共有 {len(videos)} 个视频")

def interactive_test():
    """交互式测试"""
    print("🎯 AI Manim 视频生成器 API 交互测试")
    print("=" * 50)
    
    if not test_api_status():
        return
    
    while True:
        print("\n请选择操作:")
        print("1. 生成视频")
        print("2. 查看视频列表")
        print("3. 下载视频")
        print("4. 退出")
        
        choice = input("\n👉 请输入选择 (1-4): ").strip()
        
        if choice == "1":
            content = input("📝 请输入课程内容: ").strip()
            title = input("📋 请输入标题 (可选，按Enter跳过): ").strip()
            if content:
                video_id = test_generate_video(content, title if title else None)
                if video_id:
                    download = input("是否下载视频? (y/N): ").strip().lower()
                    if download in ['y', 'yes']:
                        test_download_video(video_id)
        
        elif choice == "2":
            test_list_videos()
        
        elif choice == "3":
            video_id = input("📥 请输入视频ID: ").strip()
            if video_id:
                test_download_video(video_id)
        
        elif choice == "4":
            print("👋 退出测试")
            break
        
        else:
            print("❌ 无效选择")

if __name__ == "__main__":
    print("🚀 选择测试模式:")
    print("1. 完整自动测试")
    print("2. 交互式测试")
    
    mode = input("\n👉 请选择 (1/2): ").strip()
    
    if mode == "1":
        run_complete_test()
    elif mode == "2":
        interactive_test()
    else:
        print("❌ 无效选择") 