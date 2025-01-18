<template>
  <div v-if="showSplash" class="fixed inset-0 bg-white flex items-center justify-center z-50 overflow-hidden">
    <!-- Circle Transition Effect -->
    <div v-if="showCircleTransition" class="circle-transition"></div>

    <!-- Logo Section -->
    <transition name="fade" @after-leave="showPhoto = true">
      <img v-if="showLogo" src="@/image/splash/logo.png" alt="Logo" class="w-64 h-auto" />
    </transition>

    <!-- Photo Section -->
    <transition name="fade">
      <img v-if="showPhoto" src="@/image/splash/photo.png" alt="Photo" class="w-64 h-auto" />
    </transition>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showSplash: true,
      showLogo: true,
      showPhoto: false,
      showCircleTransition: false,
    };
  },
  mounted() {
    // Tampilkan logo selama 2 detik
    setTimeout(() => {
      this.showLogo = false;
    }, 2000);

    // Tampilkan foto selama 2 detik
    setTimeout(() => {
      this.showCircleTransition = true; // Mulai animasi circle transition
    }, 5000);

    // Sembunyikan splash screen dan navigasi ke halaman berikutnya
    setTimeout(() => {
      this.showSplash = false;
      this.$router.push('/index'); // Ganti dengan rute halaman beranda
    }, 5500); // Tambahkan delay untuk sinkronisasi dengan fade-in
  },
};
</script>

<style scoped>
/* Transisi Fade */
.fade-enter-active, .fade-leave-active {
  @apply transition-opacity duration-1000 ease-in-out;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

/* Animasi Circle */
.circle-transition {
  position: absolute;
  width: 100px;
  height: 100px;
  background-color: #fff;
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(0);
  animation: circleExpand 1s ease-in-out forwards;
  z-index: 60;
}

@keyframes circleExpand {
  to {
    transform: translate(-50%, -50%) scale(20);
  }
}
</style>
