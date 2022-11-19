import { reactive } from 'vue'
import { envs } from '@/utils'
import { httpUtils } from '@/utils'

export const store = reactive({
    user: null,
    async auth() {
        await fetch(envs.baseURL + "/authenticate", httpUtils.get())
            .then(async (resp) => {
                if (resp.status == 200) {
                    const response = await resp.json()
                    this.user = response
                }
            })
    },
    async logout() {
        this.user = null
        await fetch(envs.baseURL + "/logout", httpUtils.post())
    }
})
