<template>
  <MainLayout>
    <div class="max-w-3xl mx-auto bg-white shadow-lg rounded-lg overflow-hidden p-6 mt-3">
      <!-- Header -->
      <h1 class="text-3xl font-blackExtended mt-3 text-center mb-6">
        Tentang <br>
        <span class="bg-green-500 text-white px-2 py-1 rounded inline-block mt-1">Konserku.</span>
      </h1>

      <!-- Tentang Aplikasi -->
      <section class="mb-6">
        <h2 class="text-2xl font-blackExtended mt-3 text-gray-800 mb-2">Tentang Aplikasi</h2>
        <p class="text-gray-600 leading-relaxed">
          Aplikasi ini dirancang untuk memudahkan pengguna dalam mencari, membeli, dan mengelola tiket konser secara online. 
          Dengan antarmuka yang intuitif dan fitur-fitur yang lengkap, aplikasi ini memberikan pengalaman yang nyaman dan 
          cepat bagi pengguna.
        </p>
        <ul class="list-disc ml-6 mt-4 text-gray-600">
          <li>Cari konser sesuai lokasi, tanggal, atau artis favorit Anda.</li>
          <li>Pembayaran aman dengan berbagai metode, termasuk transfer bank dan e-wallet.</li>
          <li>Riwayat transaksi yang lengkap dan dapat diakses kapan saja.</li>
        </ul>
        
        <!-- Button Demo Aplikasi -->
        <div class="mt-6 text-center">
          <a href="https://www.youtube.com/watch?v=G_9mTt6loHU" target="_blank">
            <button class="bg-green-500 text-white px-6 py-3 rounded-full hover:bg-green-600 transition duration-200">
              Demo Aplikasi
            </button>
          </a>
        </div>
      </section>

      <!-- Tentang Pengembang -->
      <section>
        <h2 class="text-2xl font-blackExtended mt-3 text-gray-800 mb-4">Tentang Pengembang</h2>
        <div class="flex items-center gap-6 mb-6">
          <!-- Developer 1 -->
          <div class="flex items-start gap-4">
            <img
              :src="rafliImage"
              alt="Foto Pengembang 1"
              class="w-24 h-24 rounded-full object-cover border border-gray-300"
            />
            <div>
              <p class="text-gray-800 ext-1xl font-blackExtended mt-3">Rafli Nugraha <br> 15-2022-254</p>
              <p class="text-gray-600 text-sm">Pengembang Aplikasi Client</p>
              <p class="text-gray-800 font-semibold">rafli.nugraha@mhs.itenas.ac.id</p>
              <p class="text-gray-800 font-semibold">
                LinkedIn: 
                <a href="https://www.linkedin.com/in/rafli-nugraha-212193277/" class="text-blue-500 hover:underline">https://www.linkedin.com/in/rafli-nugraha-212193277/</a>
              </p>
            </div>
          </div>
        </div>

        <div class="flex items-center gap-6">
          <!-- Developer 2 -->
          <div class="flex items-start gap-4">
            <img
              :src="fahrezaImage"
              alt="Foto Pengembang 2"
              class="w-24 h-24 rounded-full object-cover border border-gray-300"
            />
            <div>
              <p class="text-gray-800 ext-1xl font-blackExtended mt-3">Fahreza Riana Atarik<br> 15-2022-238</p>
              <p class="text-gray-600 text-sm">Pengembang Aplikasi Admin</p>
              <p class="text-gray-800 font-semibold">fahreza.riana@mhs.itenas.ac.id</p>
              <p class="text-gray-800 font-semibold">
                LinkedIn: 
                <a href="https://www.linkedin.com/in/fahreza-riana-attarik-645a09248/" class="text-blue-500 hover:underline">https://www.linkedin.com/in/fahreza-riana-attarik-645a09248/</a>
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </MainLayout>
</template>

<script setup>
import MainLayout from "@/layouts/MainLayout.vue";

import rafliImage from "@/image/developer/rafli.jpg";
import fahrezaImage from "@/image/developer/fahreza.jpg";
</script>

<style scoped>
/* Tambahkan styling tambahan jika diperlukan */
</style>
