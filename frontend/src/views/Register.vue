<template>
    <div style="display: flex; width: 100vw; justify-content: center;">
        <div style="padding: 2rem; width: 100vw; max-width: 600px">
            <v-form ref="form" v-model="valid" lazy-validation>
                <v-text-field v-model="email" :rules="emailRules" label="メール" required />
                <v-text-field type="password" v-model="password" :rules="passRules" label="パスワード" required />
                <v-text-field  v-model="lastName" :rules="nameRules" label="姓" required />
                <v-text-field v-model="firstName" :rules="nameRules" label="名" required />
                <v-btn :disabled="!valid" color="success" class="mr-4" @click="validate">
                    新規登録
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
        passRules: [
            v => !!v || 'パスワードは必須項目です',
            v => (v && v.length >= 8) || 'パスワードは8文字以上入力してください',
        ],
        nameRules: [
            v => !!v || '名前は必須項目です',
        ],
        firstName: '',
        lastName: '',
        select: null,
        checkbox: false,
    }),

    methods: {
        async submit() {
            const res = await fetch(paths.register, httpUtils.post({
                'email': this.email,
                "password": this.password,
                "first_name": this.firstName,
                "last_name": this.lastName
            }))
            if (res.ok) {
                this.$router.push("/login")
            } else {
                this.$swal({
                    type: "warning",
                    text: "ユーザ登録に失敗しました"
                })
            }

        },
        validate() {
            this.$refs.form.validate()
            if (this.email && this.password && this.firstName && this.lastName && this.valid) {
                this.submit()
            }
        },
    },
}
</script>
  