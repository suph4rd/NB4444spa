const static_dir = '../vueapp_core/static/vueapp_core';
const isProduction = process.env.NODE_ENV === "production";

module.exports = {
  transpileDependencies: true,
  // publicPath: "file:///Users/andreibiarniak/PycharmProjects/NB4444vue/nb4444-vue/dist",
  publicPath: "/",
  outputDir: 'dist/',
  pluginOptions: {
    vuetify: {
			// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
		}
  }
}
