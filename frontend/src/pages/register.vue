<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useMessage } from 'naive-ui'

const router = useRouter()
const message = useMessage()
const userStore = useUserStore()

const formRef = ref()
const form = ref({ username: '', password: '' })

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

function handleRegister() {
  formRef.value?.validate((errors: any) => {
    if (errors) return
    userStore.register(form.value.username, form.value.password)
    message.success('注册成功')
    router.push('/login')
  })
}
</script>
<template>
  <n-card title="注册" style="max-width: 400px; margin: 80px auto">
    <n-form :model="form" :rules="rules" ref="formRef">
      <n-form-item label="用户名" path="username">
        <n-input v-model:value="form.username" />
      </n-form-item>
      <n-form-item label="密码" path="password">
        <n-input v-model:value="form.password" type="password" />
      </n-form-item>
    </n-form>

    <n-space justify="space-between">
      <n-button @click="router.push('/login')" tertiary>已有账号</n-button>
      <n-button type="primary" @click="handleRegister">注册</n-button>
    </n-space>
  </n-card>
</template>