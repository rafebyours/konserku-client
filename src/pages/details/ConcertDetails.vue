<template>
  <MainLayout>
    <transition
      name="slide-right"
      @before-enter="beforeEnter"
      @enter="enter"
      @leave="leave"
    >
      <div
        v-if="cardData"
        class="max-w-md mx-auto bg-white shadow-lg rounded-lg overflow-hidden p-4"
        key="slide-transition"
      >
        <div class="relative">
          <button
            @click="$router.push('/home')"
            class="btn flex items-center top-4 left-4 absolute z-10 text-white bg-black bg-opacity-60"
          >
            <i class="fas fa-arrow-left"></i>
          </button>
          <figure class="w-full h-full relative">
            <img
              :src="cardData.image"
              alt="Concert Image"
              class="w-full h-64 object-cover rounded-lg"
            />
          </figure>
        </div>

        <div class="p-4">
          <h3 class="text-gray-600 text-xs uppercase">Music Concert</h3>
          <h2 class="text-2xl font-bold mt-1">{{ cardData.title }}</h2>
          <div class="mt-2 text-lg text-gray-900 font-semibold">
            Rp. {{ formattedPrice }}
            <span class="text-sm font-normal text-gray-500">/ person</span>
          </div>
          <p class="text-sm text-gray-500">{{ cardData.description }}</p>

          <div class="mt-4 flex items-center space-x-2 text-green-500">
            <i class="fas fa-calendar-alt"></i>
            <p>{{ cardData.date }} at {{ cardData.time }}</p>
          </div>
          <div class="mt-2 flex items-center space-x-2 text-gray-700">
            <i class="fas fa-map-marker-alt text-green-500"></i>
            <p>{{ cardData.location }}</p>
            <a :href="mapDirectionUrl" class="text-green-500 underline" target="_blank">Direction</a>
          </div>

          <!-- OpenStreetMap -->
          <div id="map" 
            class="mt-4" 
            :class="{ 'pointer-events-none': showModal }"
            style="height: 300px; width: 100%; z-index: 1;">
          </div>


          <div class="mt-4">
            <h4 class="text-lg font-medium">Event Details</h4>
            <p class="text-gray-600 text-sm mt-2">{{ cardData.description }}</p>
          </div>

          <button
            @click="openModal"
            class="mt-6 w-full bg-green-500 text-white text-lg font-bold py-2 rounded-lg hover:bg-green-600"
          >
            Buy Tickets
          </button>

          <!-- Modal logic and confirmation details stay the same -->
          <div
            v-if="showModal"
            class="fixed inset-0 bg-black bg-opacity-50 flex items-end z-20"
          >
            <div
              class="relative bg-white w-full rounded-t-lg p-6 pb-16"
              style="animation: slide-up 1.0s ease-out;"
            >
              <div class="flex justify-between items-center">
                <h2 class="text-xl font-bold">Buy Tickets</h2>
                <button @click="closeModal" class="text-gray-500 hover:text-black">
                  <i class="fas fa-times"></i>
                </button>
              </div>
              <hr class="my-4" />
              <div>
                <h3 class="text-lg font-semibold">Ticket Info</h3>
                <p class="text-gray-500">Event: {{ cardData.title }}</p>
                <p class="text-gray-500">Price: Rp. {{ formattedPrice }} / ticket</p>
              </div>
              <div class="mt-4">
                <h3 class="text-lg font-semibold">Purchase Tickets</h3>
                <div class="flex items-center space-x-4 mt-2">
                  <label for="quantity" class="text-gray-600">Quantity:</label>
                  <input
                    id="quantity"
                    type="number"
                    v-model="ticketQuantity"
                    min="1"
                    class="w-16 border border-gray-300 rounded px-2 text-center"
                  />
                </div>
                <p class="text-gray-900 font-bold mt-4">
                  Total: Rp. {{ totalCost }}
                </p>
              </div>
              <button
                @click="confirmPurchase"
                class="mt-6 w-full bg-green-500 text-white text-lg font-bold py-2 rounded-lg hover:bg-green-600"
              >
                Confirm Purchase
              </button>
            </div>
          </div>



        </div>
      </div>
    </transition>
  </MainLayout>
</template>

<script setup>
import MainLayout from "@/layouts/MainLayout.vue";
import { ref, onMounted, computed, watch, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router"; // Import useRouter
import axios from "axios";
import L from "leaflet";
import "leaflet/dist/leaflet.css";



// Inisialisasi router
const router = useRouter();
const route = useRoute();
const concertId = route.params.id;
const cardData = ref(null);
const showModal = ref(false);

// Modal handling
const ticketQuantity = ref(1);

const fetchConcertData = async (id) => {
  try {
    const response = await axios.get(
      `https://api-ticketconcert.vercel.app/api/concerts/${concertId}`
    );
    cardData.value = response.data;
  } catch (error) {
    console.error("Error fetching concert data:", error);
  }
};

onMounted(() => {
  if (concertId) {
    fetchConcertData(concertId);
  }
});

const mapDirectionUrl = computed(() => {
  if (!cardData.value?.coordinates) return "#"; // Pastikan koordinat tersedia
  const { latitude, longitude } = cardData.value.coordinates;

  // Menggunakan Google Maps Directions API untuk link langsung ke lokasi
  return `https://www.google.com/maps/dir/?api=1&destination=${latitude},${longitude}`;
});


watch(
  () => cardData.value,
  (newData) => {
    if (newData && newData.coordinates) {
      const { latitude, longitude } = newData.coordinates;
      nextTick(() => {
        initMap(latitude, longitude);
      });
    }
  },
  { immediate: true }
);

const initMap = (latitude, longitude) => {
  const map = L.map("map").setView([latitude, longitude], 13);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);
  L.marker([latitude, longitude])
    .addTo(map)
    .bindPopup(cardData.value?.location || "Unknown Location")
    .openPopup();
};

const formatPrice = (price) => new Intl.NumberFormat("id-ID").format(price);
const formattedPrice = computed(() => formatPrice(cardData.value?.price || 0));

// Total cost calculation
const totalCost = computed(() => {
  return formatPrice(ticketQuantity.value * (cardData.value?.price || 0));
});

const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const confirmPurchase = () => {
  const ticketData = {
    title: cardData.value.title,
    price: cardData.value.price,
    quantity: ticketQuantity.value,
  };

  // Simpan data tiket ke localStorage
  localStorage.setItem("ticketInfo", JSON.stringify(ticketData));
  
  // Navigasi menggunakan router
  router.push("/payment");
};
</script>



<style scoped>
/* Atur z-index untuk modal dan peta */
#map {
  z-index: 1;
}

/* Tambahkan animasi slide-up */
@keyframes slide-up {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

/* Pointer-events-none untuk elemen map */
.pointer-events-none {
  pointer-events: none;
}
</style>


