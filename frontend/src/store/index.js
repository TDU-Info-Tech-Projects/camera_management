import { reactive } from 'vue'
import { paths } from '@/utils'
import { httpUtils } from '@/utils'

export const store = reactive({
    user: null,
    async auth() {
        await fetch(paths.authenticate, httpUtils.get())
            .then(async (resp) => {
                if (resp.status == 200) {
                    const response = await resp.json()
                    this.user = response
                }
            })
    },
    async logout() {
        this.user = null
        await fetch(paths.logout, httpUtils.post())
    }
})
