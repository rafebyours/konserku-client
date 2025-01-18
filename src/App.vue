<template>
  <div id="app">
    <main>
      <router-view />
      <RealtimeNotification />
    </main>
  </div>
</template>

<script>
import RealtimeNotification from './components/RealtimeNotification.vue';

export default {
  components: {
    RealtimeNotification,
  },
};
</script>

<style scoped>
/* Add any global styles here */
</style>
