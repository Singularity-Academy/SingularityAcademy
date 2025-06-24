<template>
  <div class="home-page">
    <div class="hero">
      <div class="hero-content">
        <h1 class="hero-title">
          {{ typedText }}<span v-if="showCursor" class="cursor">|</span>
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
        <img src="~/assets/illus/illus_hero_25.png" alt="illustration" />
      </div>
    </div>

    <div class="section">
      <n-h2 prefix="bar">平台特色</n-h2>
      <n-grid :cols="cols" :x-gap="20" :y-gap="20">
        <n-gi v-for="(feature, index) in features" :key="index">
          <div class="feature-card">
            <n-card :title="feature.title" hoverable>
              {{ feature.description }}
            </n-card>
          </div>
        </n-gi>
      </n-grid>
    </div>

    <div class="section">
      <n-h2 prefix="bar">我们的愿景</n-h2>
      <div class="vision-list">
        <p v-for="(vision, index) in visions" :key="index" :class="'vision-text ' + vision.color">
          {{ vision.content }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'

const fullText = '欢迎来到 ClarifAI - “看见” 学习，为你而来。'
const typedText = ref('')
const showCursor = ref(true)

const router = useRouter()
const goTo = (path: string) => router.push(path)

const cols = ref(2)
const updateCols = () => {
  cols.value = window.innerWidth < 640 ? 1 : 2
}

onMounted(() => {
  updateCols()
  window.addEventListener('resize', updateCols)
  let index = 0
  const typingInterval = setInterval(() => {
    if (index < fullText.length) {
      typedText.value += fullText[index++]
    } else {
      clearInterval(typingInterval)
    }
  }, 100)
  setInterval(() => {
    showCursor.value = !showCursor.value
  }, 500)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateCols)
})

const features = [
  { title: 'AI 智能学习', description: '体验个性化教育，配备前沿人工智能技术，适应您的学习风格。', icon: '🧠' },
  { title: '互动体验', description: '参与沉浸式学习环境，让复杂概念变得易于理解。', icon: '🎯' },
  { title: '全球社区', description: '与全世界的学习者连接，在我们充满活力的教育生态系统中分享知识。', icon: '🌍' },
  { title: '刨根问底', description: '我们提供深入的解析，帮助你理解复杂的概念。', icon: '📊' }
]

const visions: { content: string; color: 'red' | 'white' }[] = [
  { content: '我们致力于通过AI技术打破教育壁垒，让优质教育资源触手可及', color: 'white' },
  { content: '教育不应是奢侈品！我们为需要帮助的学习者提供完全免费的顶级教育资源', color: 'red' }
]

</script>

<style scoped lang="scss">
.home-page {
  padding: 2.5rem;
  background: var(--main-bg);
}

.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 3.75rem 0;
  background: url('@/assets/background.png') no-repeat center center;
  background-size: cover;
  flex-wrap: wrap;
}

.hero-content {
  max-width: 37.5rem;
}

.hero-title {
  font-size: 2.25rem;
  font-weight: 800;
  line-height: 1.5;
}

.hero-description {
  font-size: 1.125rem;
  color: #666;
  margin: 1.25rem 0;
}

.hero-image img {
  width: 22.5rem;
}

.section {
  padding: 3.75rem 0;
}

.cursor {
  display: inline-block;
  width: 1px;
  background-color: #333;
  animation: blink 1s step-end infinite;
}

.vision-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
}

.vision-text {
  font-size: 1.125rem;
  max-width: 720px;
  text-align: center;
  padding: 0.75rem 1rem;
  border-radius: 6px;
}

.vision-text.red {
  background-color: #fff1f0;
  color: #a8071a;
  border-left: 4px solid #cf1322;
}

.vision-text.white {
  background-color: #ffffff;
  color: #333333;
  border-left: 4px solid #b6b4b4;
}

.feature-card {
  max-width: 750px;
  margin: 0 auto;
}

@keyframes blink {

  from,
  to {
    opacity: 1;
  }

  50% {
    opacity: 0;
  }
}
</style>
