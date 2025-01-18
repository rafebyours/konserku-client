<template>
  <MainLayout>
    <transition
      name="fade"
      @before-enter="beforeEnter"
      @enter="enter"
      @leave="leave"
    >
      <div
        v-if="isVisible"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 w-full px-4 items-start overflow-auto"
        key="home-content"
      >
        <div class="flex flex-col">
          <h1 class="text-1xl font-blackExtended mt-3">
            Hello, <span class="bg-green-500 text-white px-2 py-1 rounded">{{ username }} !</span>
          </h1>

          <h2 class="text-2xl font-blackExtended mt-5">Upcoming Event</h2>
        </div>
      </div>
    </transition>

    <div class="flex overflow-x-auto p-4 gap-4">
      <div class="flex gap-4">
        <!-- Render Skeleton Loader or Concert Cards -->
        <div
          v-if="loadingConcerts"
          class="card w-60 bg-base-100 image-full shadow-xl mt-2 flex-shrink-0 mb-4"
        >
          <div class="skeleton-loader h-full w-full bg-gray-300"></div>
        </div>

        <!-- Render Concert Cards Dynamically -->
        <div
          v-for="(card, index) in concerts"
          :key="index"
          class="card w-60 bg-base-100 image-full shadow-xl mt-2 flex-shrink-0 mb-4"
          @click="navigateToConcertDetails(card._id)"
        >
          <figure class="w-full h-full relative">
            <img :src="card.image" alt="Concert" class="w-full h-full object-cover" />
            <div class="absolute inset-0 bg-black opacity-40"></div>
          </figure>
          <div class="card-body relative z-10">
            <h2 class="card-title font-sans2 text-white">{{ card.title }}</h2>
            <p class="font-sans text-white custom-shadow">
              {{ card.date }} <br />
              {{ card.location }} <br />
              <span v-if="isLongText(card.description)">
                ... <router-link :to="`/concert/${card._id}`" class="text-blue-500">See More</router-link>
              </span>
            </p>
            <div class="card-actions justify-end">
              <router-link
                :to="`/concert/${card._id}`"
                class="btn glass font-sans text-white custom-shadow"
              >
                Buy Tickets
              </router-link>
            </div>
          </div>
        </div>

      </div>
    </div>

    <div class="text-center mt-4">
      <h2 class="text-2xl font-blackExtended mt-5">Near Bandung</h2>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 w-full mt-4">
      <div
        v-if="loadingFilteredCards"
        class="card w-full bg-base-100 image-full mt-1 mb-4 p-4"
      >
        <div class="skeleton-loader h-full w-full bg-gray-300"></div>
      </div>

      <!-- Render Filtered Concert Cards -->
      <div
        v-for="(card, index) in filteredCards"
        :key="index"
        class="card w-full bg-base-100 image-full mt-1 mb-4 p-4"
        @click="saveCardData(card)"
      >
        <figure class="w-full h-full relative">
          <img :src="card.image" alt="Concert" class="w-full h-full object-cover" />
          <div class="absolute inset-0 bg-black opacity-40"></div>
        </figure>
        <div class="card-body relative z-10">
          <h2 class="card-title font-sans2 text-white">{{ card.title }}</h2>
          <p class="font-sans text-white custom-shadow">
            {{ card.date }} <br />
            {{ card.location }} <br />
            <span v-if="isLongText(card.description)">
              ... <router-link :to="`/concert/${card._id}`" class="text-blue-500">See More</router-link>
            </span>
          </p>
          <div class="card-actions justify-end">
            <router-link
              :to="`/concert/${card._id}`"
              class="btn glass font-sans text-white custom-shadow"
            >
              Buy Tickets
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import MainLayout from "@/layouts/MainLayout.vue";
import { ref, onMounted, computed } from "vue";
import { useRouter } from 'vue-router';
import axios from 'axios';

const concerts = ref([]);  // Untuk menyimpan data konser
const filteredCards = computed(() => concerts.value.filter(card => card.city === 'Bandung'));  // Filter konser yang ada di Bandung
const isVisible = ref(false);
const username = ref('');
const loadingConcerts = ref(true); // Track if concerts are loading
const loadingFilteredCards = ref(true); // Track if filtered concerts are loading

// Fungsi untuk mendapatkan informasi pengguna
const getUserInfo = () => {
  const userId = localStorage.getItem('user_id');
  const storedUsername = localStorage.getItem('username');
  
  if (userId && storedUsername) {
    username.value = storedUsername;
  } else {
    // Jika tidak ada user_id atau username di localStorage, redirect ke halaman login
    router.push('/login');
  }
};

// Ambil data konser dari API
const fetchConcerts = async () => {
  try {
    const response = await axios.get('https://api-ticketconcert.vercel.app/api/concerts');
    concerts.value = response.data;
    console.log('Concerts data:', concerts.value); // Tambahkan log untuk debug
        // Setelah data konser selesai dimuat, set isVisible menjadi true
        isVisible.value = true;
        loadingConcerts.value = false; // Set loading to false after data is fetched
  } catch (error) {
    console.error('Error fetching concerts:', error);
  }
};

// Ambil data konser yang difilter
const fetchFilteredCards = async () => {
  try {
    const response = await axios.get('https://api-ticketconcert.vercel.app/api/concerts');
    filteredCards.value = response.data.filter((card) => card.city === 'Bandung');
    loadingFilteredCards.value = false; // Set loading to false after filtered cards are fetched
  } catch (error) {
    console.error('Error fetching filtered cards:', error);
  }
};

// Fungsi untuk menyimpan data kartu konser yang dipilih ke localStorage
// Fungsi untuk menyimpan data kartu konser yang dipilih dan mengarahkan ke halaman detail
const saveCardData = (cardData) => {
  localStorage.setItem("selectedCard", JSON.stringify(cardData));  // Menyimpan data kartu
  router.push(`/concert/${cardData._id}`);  // Mengarahkan ke halaman detail dengan ID konser menggunakan path langsung
};

const navigateToConcertDetails = (concertId) => {
  if (!concertId) {
    console.error('Concert ID is missing!');
    return;
  }

  // Simpan data ke localStorage (jika diperlukan)
  const selectedCard = concerts.value.find(card => card._id === concertId);
  if (selectedCard) {
    localStorage.setItem("selectedCard", JSON.stringify(selectedCard));
  }

  // Navigasi ke halaman detail konser
  router.push(`/concert/${concertId}`);
};

// Fungsi untuk memeriksa jika teks terlalu panjang
const isLongText = (text) => text.length > 20;

onMounted(() => {
  getUserInfo();  // Mendapatkan informasi pengguna
  fetchConcerts();  // Mengambil data konser saat halaman dimuat
  fetchFilteredCards(); // Mengambil data konser yang difilter
});
</script>

<style lang="scss" scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter,
.fade-leave-to {
  opacity: 0;
}
.card-fixed-size {
  width: 250px;
  height: 250px;
  flex-shrink: 0;
}

/* Skeleton Loader */
.skeleton-loader {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.card {
  height: 350px; /* Set fixed height for card */
}

.card figure img {
  object-fit: cover; /* Ensure the image covers the full area */
  height: 100%;
  width: 100%;
}
</style>
