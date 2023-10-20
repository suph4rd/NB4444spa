export default {
  data: function () {
      return {
          createPath: null,
          dialogCreate: false,
          // обязательные параметры! this.$apiHost this.apiPath
      };
  },

  mounted() {
      this.preMount();
      this.getObject();
      this.postMount();
  },

  methods: {

      getFormParams() {
        throw "Not implemented";
      },

      resetForm() {
        throw "Not implemented";
      },

      redirectLogic() {
          throw "Not implemented"
      },

      getObject() {},

      preMount() {},

      postMount() {},

      sendForm(e) {
        e.preventDefault();
        let headers = this.getHeaders();
        let data = this.getFormParams();
          this.axios.post( `${this.$apiHost}${this.createPath}`, data, {
              headers: headers
            }).then((res) => {
                this.resetForm();
                this.redirectLogic();
            }).catch((res) => {
            this.dropSession(res);
          });
      },

  }
}