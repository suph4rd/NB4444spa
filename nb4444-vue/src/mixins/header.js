export default {
    methods: {
        getHeaders() {
            return {
                'Content-Type': 'application/json',
            };
        },
        dropSession(res) {
            const status = res && res.response && res.response.status

            if (status === 401) {
                this.$store.commit('clearUser')
                if (this.$route.name !== 'Login') {
                    this.$router.replace({
                        name: 'Login',
                        query: { redirect: this.$route.fullPath },
                    })
                }
                return
            }

            if (res && res.response) {
                alert(`status: ${status} message: ${res.response.statusText}`)
            } else {
                console.error(res)
            }
        },
    }
}
