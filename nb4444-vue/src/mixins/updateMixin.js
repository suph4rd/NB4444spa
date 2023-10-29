import {th} from "vuetify/locale";

export default {
  data () {
    return {
      object: null,
      defaultObject: null,
      updatePath: null,
    };
  },

    mounted() {
      this.preMount();
      this.getObject();
      this.postMount();
    },

    methods: {

      getUpdatePath() {
          throw "Not implemented";
      },

      getFormParams() {
          throw "Not implemented";
      },

      resetForm() {
          throw "Not implemented";
      },

      redirectLogic(res) {
          throw "Not implemented"
      },

      preMount() {},

      postMount() {},

      getObject() {
        let headers = this.getHeaders();
        this.axios.get(this.getUpdatePath(), {
          headers: headers
        }).then((result) =>{
          console.log(result.data);
          this.defaultObject = result.data;
          this.object = Object.assign({}, this.defaultObject);
        }).catch((res) => {
            this.dropSession(res);
        });
      },

      sendForm(e) {
        e.preventDefault();
        let headers = this.getHeaders();
        let data = this.getFormParams();
          this.axios.patch(this.getUpdatePath(), data, {
              headers: headers
            }).then((res) => {
                this.resetForm();
                this.redirectLogic(res);
            }).catch((res) => {
                this.dropSession(res);
          });
      },

  },
}