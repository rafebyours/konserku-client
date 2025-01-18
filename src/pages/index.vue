<template>
  <transition 
    name="fade" 
    @before-enter="beforeEnter" 
    @enter="enter" 
    @leave="leave">
    <div v-if="isVisible" class="flex flex-col h-screen w-screen justify-between items-center bg-cover bg-center bg-custom">
      <h1 class="text-2xl font-sans2"></h1>
      <div class="flex w-full px-4 flex-col justify-end items-center">
        <!-- Tautan Video -->
        <a href="https://www.youtube.com/watch?v=G_9mTt6loHU" target="_blank" class="text-black text-lg mb-4 underline hover:text-decoration-color-green-500 hover:underline">
          Link video demo aplikasi
        </a>

        <!-- Tombol Masuk -->
        <button @click="$router.push('/login')" class="flex items-center justify-between bg-black text-white px-6 py-3 rounded-md w-full max-w-sm text-lg font-sans mb-8 transition duration-200 hover:bg-gray-800">
          <span>Masuk</span>
          <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3"></path>
          </svg>
        </button>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const isVisible = ref(false);

// Control the visibility to trigger the transition
onMounted(() => {
  setTimeout(() => {
    isVisible.value = true;  // Trigger visibility after timeout to allow the fade-in effect
  }, 500);  // Delay if necessary
});

const beforeEnter = (el) => {
  el.style.opacity = 0;  // Ensure element starts as invisible
};

const enter = (el, done) => {
  el.offsetHeight;  // Trigger reflow
  el.style.transition = "opacity 1s ease";  // Duration of transition
  el.style.opacity = 1;  // Fade in effect
  done();
};

const leave = (el, done) => {
  el.style.transition = "opacity 1s ease";  // Duration of transition
  el.style.opacity = 0;  // Fade out effect
  done();
};
</script>

<style lang="scss" scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 1s ease;  // Apply transition to opacity
}

.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}

.custom-underline:hover {
  text-decoration-color: #22c55e; /* Warna green-500 Tailwind */
}

a {
  text-decoration-color: black; /* Menetapkan warna underline default ke hitam */
}

a:hover {
  text-decoration-color: #22c55e; /* Mengubah warna underline saat hover menjadi hijau */
}

/* Add this rule to set the background image */
.bg-custom {
  background-image: url('@/image/bg/bg-index.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
</style>
