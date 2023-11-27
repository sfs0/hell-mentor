<template>
  <!-- container -->


  <router-view />
</template>

<script>
import Nav from '@/components/Nav.vue';

export default {
  name: 'App',
  components: {
    Nav,
  },
  data() {
    return {

    };
  },
};
</script>

<style>
html,
body {
  /* overflow: hidden; */
  margin: 0;
  padding: 0;
}
</style>
