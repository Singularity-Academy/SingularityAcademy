<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useMessage } from 'naive-ui'

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

function handleRegister() {
  formRef.value?.validate((errors: any) => {
    if (errors) return
    userStore.register(form.value.username, form.value.password)
    message.success(t('api.auth.registrationSuccessful'))
    router.push('/auth/login')
  })
}
</script>

<template>
  <n-card :title="t('common.signUp')" style="max-width: 400px; margin: 80px auto">
    <n-form :model="form" :rules="rules" ref="formRef">
      <n-form-item :label="t('common.fullName')" path="username">
        <n-input v-model:value="form.username" />
      </n-form-item>
      <n-form-item :label="t('common.password')" path="password">
        <n-input v-model:value="form.password" type="password" />
      </n-form-item>
    </n-form>

    <n-space justify="space-between">
      <n-button @click="router.push('/auth/login')" tertiary>{{ t('LoginPage.doNotHaveAnAccount') }}</n-button>
      <n-button type="primary" @click="handleRegister">{{ t('common.signUp') }}</n-button>
    </n-space>
  </n-card>
</template>
