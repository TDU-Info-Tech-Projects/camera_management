<template>
    <div style="display: flex; width: 100vw; justify-content: center;">
        <div style="padding: 2rem; width: 100vw; max-width: 600px">
            <v-form ref="form" v-model="valid" lazy-validation>
                <v-text-field v-model="email" :rules="emailRules" label="メール" required></v-text-field>
                <v-text-field type="password" v-model="password" :rules="nameRules" label="パスワード" required>
                </v-text-field>
                <v-btn :disabled="!valid" color="success" class="mr-4" @click="validate">
                    ログイン
                </v-btn>
            </v-form>
        </div>
    </div>
</template>

<script>
import { paths } from '@/utils'
import { httpUtils } from '@/utils'

export default {
    data: () => ({
        valid: false,
        email: '',
        emailRules: [
            v => !!v || 'メールは必須項目です',
            v => /.+@.+\..+/.test(v) || '正しいメールアドレスを入力してください',
        ],
        password: '',
        nameRules: [
            v => !!v || 'パスワードは必須項目です',
            v => (v && v.length >= 8) || 'パスワードは8文字以上入力してください',
        ],
        select: null,
        checkbox: false,
    }),

    methods: {
        async submit() {
            const res = await fetch(paths.login, httpUtils.post({
                'email': this.email,
                "password": this.password,
            }))
            if (res.ok) {
                this.$router.push(this.$route.query.redirect || "/")
            } else {
                this.$swal({
                    type: "warning",
                    text: "ログインに失敗しました"
                })
            }

        },
        validate() {
            this.$refs.form.validate()
            if (this.email && this.password && this.valid) {
                this.submit()
            }
        },
    },
}
</script>
  