<template>
    <section class="flex flex-col min-h-screen">
      <Header />
      <main class="flex-grow overflow-scroll bg-gray-50 pb-16"> <!-- Tambahkan pb-16 -->
        <slot />
      </main>
      <Navbar class="fixed bottom-0 w-full" /> <!-- Tetap menggunakan fixed -->
    </section>
  </template>
  
  <script setup>
  import Header from "@/components/header/index.vue";
  import Navbar from "@/components/navbar/index.vue";
  </script>
  
  <style lang="scss" scoped>
  /* Anda dapat menyesuaikan style tambahan jika diperlukan */
  </style>
  