import { defineStore } from 'pinia'
export const useUserStore = defineStore('user', {
    state: () => ({
        token: '',
        username: ''
    }),

    actions: {
        login(username: string) {
            // 登录验证
            this.token = ''
            this.username = username
        },

        logout() {
            // 清除登录
            this.token = ''
            this.username = ''
        },

        register(username: string, password: string) {
            // 注册
        }
    },

    getters: {
        isLoggedIn: state => !!state.token
    }
})
