#!/usr/bin/env python3
"""
AI Manim API 测试客户端
测试文字输入到视频输出的功能
"""

import requests
import json
import time
import os

API_BASE = "http://localhost:8888"

def test_api_connection():
    """测试API连接"""
    print("🔗 测试API连接...")
    try:
        response = requests.get(f"{API_BASE}/")
        if response.status_code == 200:
            data = response.json()
            print("✅ API连接成功")
            print(f"   服务: {data['service']}")
            print(f"   版本: {data['version']}")
            print(f"   AI状态: {data['ai_status']}")
            return True
        else:
            print(f"❌ API响应异常: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API，请确认服务器已启动")
        return False
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False

def test_generate_video(text_input, title=None, model=None):
    """测试视频生成"""
    print(f"\n🎬 测试视频生成")
    print(f"📝 输入文字: {text_input}")
    if title:
        print(f"📋 标题: {title}")
    if model:
        print(f"🤖 指定模型: {model}")
    
    # 构建请求数据
    payload = {"text": text_input}
    if title:
        payload["title"] = title
    if model:
        payload["model"] = model
    
    try:
        print("📤 发送生成请求...")
        start_time = time.time()
        
        response = requests.post(
            f"{API_BASE}/generate",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=300  # 5分钟超时
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"📥 响应时间: {duration:.1f}秒")
        print(f"📊 响应状态: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ 视频生成成功！")
                print(f"   🆔 视频ID: {data['video_id']}")
                print(f"   📁 文件大小: {data['video_size']}")
                print(f"   📥 下载链接: {API_BASE}{data['download_url']}")
                print(f"   🎭 场景名: {data.get('scene_name', 'Unknown')}")
                print(f"   🤖 使用模型: {data.get('model_used', 'Unknown')}")
                return data['video_id']
            else:
                print("❌ 视频生成失败")
                print(f"   错误: {data.get('error', '未知错误')}")
                return None
        else:
            try:
                error_data = response.json()
                print(f"❌ 生成失败: {error_data.get('error', '未知错误')}")
            except:
                print(f"❌ 生成失败: HTTP {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        print("⏰ 请求超时，视频生成可能需要更长时间")
        return None
    except Exception as e:
        print(f"❌ 生成异常: {e}")
        return None

def test_download_video(video_id, save_path=None):
    """测试视频下载"""
    print(f"\n📥 测试视频下载: {video_id}")
    
    try:
        response = requests.get(f"{API_BASE}/video/{video_id}")
        
        if response.status_code == 200:
            # 确定保存路径
            if not save_path:
                save_path = f"downloaded_{video_id}.mp4"
            
            # 保存视频文件
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            file_size = len(response.content)
            print(f"✅ 视频下载成功")
            print(f"   📁 保存路径: {save_path}")
            print(f"   📊 文件大小: {file_size/1024:.1f} KB")
            
            # 验证文件
            if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
                print(f"   ✅ 文件验证通过")
                return save_path
            else:
                print(f"   ❌ 文件验证失败")
                return None
        else:
            print(f"❌ 下载失败: HTTP {response.status_code}")
            try:
                error_data = response.json()
                print(f"   错误: {error_data.get('error', '未知错误')}")
            except:
                pass
            return None
            
    except Exception as e:
        print(f"❌ 下载异常: {e}")
        return None

def test_list_videos():
    """测试视频列表"""
    print(f"\n📋 测试视频列表...")
    
    try:
        response = requests.get(f"{API_BASE}/videos")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 获取视频列表成功")
            print(f"   📊 总数: {data['total']} 个视频")
            
            if data['videos']:
                print("   📽️ 最近的视频:")
                for i, video in enumerate(data['videos'][:3]):  # 显示前3个
                    print(f"      {i+1}. {video['video_id']}: {video['input_text'][:20]}... ({video['file_size']})")
            
            return data['videos']
        else:
            print(f"❌ 获取列表失败: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ 列表获取异常: {e}")
        return []

def test_api_status():
    """测试API状态"""
    print(f"\n🔍 测试API状态...")
    
    try:
        response = requests.get(f"{API_BASE}/status")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API状态正常")
            print(f"   🤖 AI生成器: {data['ai_generator']}")
            print(f"   📁 输出目录: {data['config']['output_dir']}")
            print(f"   📏 最大长度: {data['config']['max_content_length']}字符")
            print(f"   🔢 可用模型数: {len(data.get('models', []))}")
            
            if data.get('models'):
                print(f"   🤖 可用模型: {', '.join(data['models'])}")
            
            return True
        else:
            print(f"❌ 状态检查失败: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 状态检查异常: {e}")
        return False

def run_complete_test():
    """运行完整测试流程"""
    print("🧪 AI Manim API 完整测试")
    print("=" * 60)
    
    # 1. 测试连接
    if not test_api_connection():
        print("\n❌ API连接失败，停止测试")
        return
    
    # 2. 测试状态
    if not test_api_status():
        print("\n⚠️ API状态异常，继续测试...")
    
    # 3. 测试视频生成
    test_cases = [
        ("牛顿第一定律", "物理课程"),
        ("圆周运动", None),
        ("三角函数图像", "数学课程")
    ]
    
    generated_videos = []
    
    for text, title in test_cases:
        print("\n" + "-" * 40)
        video_id = test_generate_video(text, title)
        if video_id:
            generated_videos.append(video_id)
            
            # 等待一下再进行下一个测试
            time.sleep(3)
    
    # 4. 测试视频列表
    test_list_videos()
    
    # 5. 测试视频下载
    if generated_videos:
        print("\n" + "-" * 40)
        video_id = generated_videos[0]  # 下载第一个生成的视频
        downloaded_file = test_download_video(video_id)
        
        if downloaded_file:
            print(f"\n🎉 测试成功！生成并下载了视频: {downloaded_file}")
    
    # 6. 测试总结
    print("\n" + "=" * 60)
    print("🎉 API测试完成！")
    print(f"✅ 成功生成 {len(generated_videos)} 个视频")
    
    if generated_videos:
        print("📋 生成的视频ID:")
        for i, vid in enumerate(generated_videos, 1):
            print(f"   {i}. {vid}")
    
    print("\n💡 使用提示:")
    print("   - 访问 http://localhost:8888/ 查看API文档")
    print("   - 使用 POST /generate 生成视频")
    print("   - 使用 GET /video/{id} 下载视频")

def interactive_test():
    """交互式测试"""
    print("🎯 AI Manim API 交互式测试")
    print("=" * 50)
    
    if not test_api_connection():
        return
    
    while True:
        print("\n请选择操作:")
        print("1. 生成视频")
        print("2. 查看视频列表")
        print("3. 下载视频")
        print("4. 检查API状态")
        print("5. 退出")
        
        choice = input("\n👉 请选择 (1-5): ").strip()
        
        if choice == "1":
            text = input("📝 请输入课程内容: ").strip()
            if not text:
                print("❌ 内容不能为空")
                continue
                
            title = input("📋 请输入标题 (可选): ").strip()
            title = title if title else None
            
            model = input("🤖 请输入模型名 (可选): ").strip()
            model = model if model else None
            
            video_id = test_generate_video(text, title, model)
            
            if video_id:
                download = input("是否立即下载? (y/N): ").strip().lower()
                if download in ['y', 'yes']:
                    test_download_video(video_id)
        
        elif choice == "2":
            test_list_videos()
        
        elif choice == "3":
            video_id = input("📥 请输入视频ID: ").strip()
            if video_id:
                save_path = input("💾 保存路径 (可选): ").strip()
                save_path = save_path if save_path else None
                test_download_video(video_id, save_path)
        
        elif choice == "4":
            test_api_status()
        
        elif choice == "5":
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
        print("❌ 无效选择，运行完整测试")
        run_complete_test() 