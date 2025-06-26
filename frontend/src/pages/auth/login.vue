<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useMessage } from 'naive-ui'
import { useI18n } from 'vue-i18n'

const router = useRouter()
const message = useMessage()
const userStore = useUserStore()

const { t } = useI18n()

const formRef = ref()
const form = ref({ username: '', password: '' })

const rules = {
  username: [{ required: true, message: t('auth.nameIsRequired'), trigger: 'blur' }],
  password: [{ required: true, message: t('auth.passwordIsRequired'), trigger: 'blur' }]
}

function handleLogin() {
  formRef.value?.validate((errors: any) => {
    if (errors) return
    userStore.login(form.value.username)
    message.success(t('api.auth.loginSuccessful'))
    router.push('/')
  })
}
</script>

<template>
  <n-card :title="t('common.signIn')" style="max-width: 400px; margin: 80px auto">
    <n-form :model="form" :rules="rules" ref="formRef">
      <n-form-item :label="t('common.fullName')" path="username">
        <n-input v-model:value="form.username" />
      </n-form-item>
      <n-form-item :label="t('common.password')" path="password">
        <n-input v-model:value="form.password" type="password" />
      </n-form-item>
    </n-form>

    <n-space justify="space-between">
      <n-button @click="router.push('/auth/register')" tertiary>{{ t('RegisterPage.createAccount') }}</n-button>
      <n-button type="primary" @click="handleLogin">{{ t('common.signIn') }}</n-button>
    </n-space>
  </n-card>
</template>
