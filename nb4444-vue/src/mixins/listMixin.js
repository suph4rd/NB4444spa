export default {
  data: function () {
      return {
          data: null,
          // обязательные параметры! this.$apiHost this.apiPath
      };
  },
  mounted() {
    this.getData();
  },
  methods: {
    getData() {
        let headers = this.getHeaders();
        this.axios.get(`${this.$apiHost}${this.apiPath}`, {
          headers: headers
        }).then((result) =>{
          console.log(result.data);
          this.objects = result.data;
        }).catch((res) => {
            this.dropSession(res);
        });
    },
  }
}