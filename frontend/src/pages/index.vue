<template>
  <div class="home-page">
    <div class="hero">
      <div class="hero-content">
        <h1 class="hero-title">
          欢迎来到 ClarifAI - <span class="highlight">“看见”</span> 学习，为你而来。
        </h1>
        <p class="hero-description">
          首个 AI 教育平台，生成个性化知识视频，规划循序渐进的课程，为您提供系统性知识
        </p>
        <n-space :size="20">
          <n-button type="primary" size="large" @click="goTo('/register')">
            开始学习
          </n-button>
          <n-button size="large" @click="goTo('/login')">
            探索演示
          </n-button>
        </n-space>
      </div>
      <div class="hero-image">
        <img src="" alt="illustration" />
      </div>
    </div>

    <div class="section">
      <n-h2 prefix="bar">平台特色</n-h2>
      <n-grid :cols="3" :x-gap="20" :y-gap="20">
        <n-gi v-for="(feature, index) in features" :key="index">
          <n-card :title="feature.title" hoverable>
            {{ feature.description }}
          </n-card>
        </n-gi>
      </n-grid>
    </div>

    <div class="section">
      <n-h2 prefix="bar">我们的愿景</n-h2>
      <div class="vision-list">
        <n-tag v-for="(vision, index) in visions" :key="index" :type="vision.color" size="large" style="margin: 8px">
          {{ vision.content }}
        </n-tag>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goTo = (path: string) => {
  router.push(path)
}

const features = [
  { title: 'AI 智能学习', description: '体验个性化教育，配备前沿人工智能技术，适应您的学习风格。', icon: '🧠' },
  { title: '互动体验', description: '参与沉浸式学习环境，让复杂概念变得易于理解。', icon: '🎯' },
  { title: '全球社区', description: '与全世界的学习者连接，在我们充满活力的教育生态系统中分享知识。', icon: '🌍' },
  { title: '刨根问底', description: '我们提供深入的解析，帮助你理解复杂的概念。', icon: '📊' }
]

const visions: { content: string; color: 'success' | 'info' | 'warning' }[] = [
  { content: '我们致力于通过AI技术打破教育壁垒，让优质教育资源触手可及', color: 'success' },
  { content: '教育不应是奢侈品！我们为需要帮助的学习者提供完全免费的顶级教育资源', color: 'warning' }
]
</script>

<style scoped>
.home-page {
  padding: 40px;
  background: #fef6f2;
}

.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 60px 0;
  background: url('@/assets/background.png') no-repeat center center;
  background-size: cover;
}

.hero-content {
  max-width: 600px;
}

.hero-title {
  font-size: 36px;
  font-weight: 800;
  line-height: 1.5;
}

.hero-description {
  font-size: 18px;
  color: #666;
  margin: 20px 0;
}

.highlight {
  color: #f36f45;
}

.hero-image img {
  width: 360px;
}

.section {
  padding: 60px 0;
}

.vision-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
</style>
