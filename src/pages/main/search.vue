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
          <h2 class="text-2xl font-blackExtended mt-5">Search</h2>
        </div>

        <!-- Search Input -->
        <div class="flex gap-3 items-center w-full mt-4">
          <label class="input input-bordered flex items-center gap-3 grow">
            <input
              type="text"
              v-model="searchQuery"
              class="grow z-50"
              placeholder="Search"
            />
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 16 16"
              fill="currentColor"
              class="h-4 w-4 opacity-70"
            >
              <path
                fill-rule="evenodd"
                d="M9.965 11.026a5 5 0 1 1 1.06-1.06l2.755 2.754a.75.75 0 1 1-1.06 1.06l-2.755-2.754ZM10.5 7a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0Z"
                clip-rule="evenodd"
              />
            </svg>
          </label>
          <button @click="showFilterModal = true" class="btn btn-outline">
            Filter
          </button>
        </div>

        <!-- Filter Modal -->
        <div
          v-if="showFilterModal"
          class="fixed inset-0 bg-gray-800 bg-opacity-75 flex items-center justify-center z-50"
        >
          <div class="bg-white p-6 rounded-md w-80 overflow-y-auto">
            <h2 class="text-lg font-semibold mb-4">Filter Options</h2>
            <!-- Province Filter -->
            <label class="block mb-2">Province</label>
            <select
              v-model="selectedProvince"
              @change="fetchCities(selectedProvince)"
              class="input input-bordered w-full mb-4"
            >
              <option disabled value="">Select Province</option>
              <option v-for="province in provinces" :key="province.id" :value="province.name">
                {{ province.name }}
              </option>
            </select>

            <!-- City Filter -->
            <label class="block mb-2">City</label>
            <select
              v-model="selectedCity"
              class="input input-bordered w-full mb-4"
              :disabled="!selectedProvince"
            >
              <option disabled value="">Select City</option>
              <option v-for="city in cities" :key="city.id" :value="city.name">
                {{ city.name }}
              </option>
            </select>

            <!-- Date Range Filter -->
            <label class="block mb-2">Date Range</label>
            <div class="gap-3 mb-4">
              From
              <input
                type="date"
                v-model="startDate"
                class="input input-bordered w-full mb-4"
              />
              To
              <input
                type="date"
                v-model="endDate"
                class="input input-bordered w-full"
              />
            </div>

            <div class="flex justify-between gap-2 mt-4">
              <button
                @click="showFilterModal = false"
                class="btn btn-outline text-white bg-red-500 hover:bg-red-700"
              >
                Close
              </button>
              <button
                @click="clearFilters"
                class="btn btn-outline text-white bg-orange-500 hover:bg-orange-700"
              >
                Clear
              </button>
              <button
                @click="applyFiltersAndClose"
                class="btn btn-outline text-white bg-green-500 hover:bg-green-700"
              >
                Apply
              </button>
            </div>
          </div>
        </div>

        <!-- Card Grid -->
        <div
          class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 w-full mt-4"
        >
          <!-- Display Skeleton Loader if data is loading -->
          <div
            v-if="cards.length === 0"
            v-for="index in 6"
            :key="'loader-' + index"
            class="card w-full bg-base-100 image-full shadow-xl mt-2 mb-4"
          >
            <div class="skeleton-card">
              <div class="skeleton-image"></div>
              <div class="skeleton-text"></div>
              <div class="skeleton-text"></div>
            </div>
          </div>

          <!-- Render Cards Dynamically -->
          <div
            v-for="(card, index) in filteredCards"
            :key="index"
            class="card w-full bg-base-100 image-full shadow-xl mt-2 mb-4"
            @click="saveCardData(card)"
          >
            <figure class="w-full h-full relative">
              <img
                :src="card.image"
                alt="Concert"
                class="w-full h-full object-cover"
              />
              <div class="absolute inset-0 bg-black opacity-40"></div>
            </figure>
            <div class="card-body relative z-10">
              <h2 class="card-title font-sans2 text-white">{{ card.title }}</h2>
              <p class="font-sans text-white">
                {{ card.date }} <br />
                {{ card.location }}
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
    </transition>
  </MainLayout>
</template>

<script setup>
import MainLayout from "@/layouts/MainLayout.vue";
import { ref, computed, onMounted } from "vue";
import axios from "axios";

const cards = ref([]);
const provinces = ref([]);
const cities = ref([]);
const selectedProvince = ref("");
const selectedCity = ref("");
const startDate = ref("");
const endDate = ref("");
const searchQuery = ref("");
const showFilterModal = ref(false);
const isVisible = ref(false);

const fetchConcerts = async () => {
  try {
    const response = await axios.get("https://api-ticketconcert.vercel.app/api/concerts");
    cards.value = response.data;
    console.log("Concert data:", cards.value); // Debug log
  } catch (error) {
    console.error("Error fetching concerts:", error);
  }
};

const fetchProvinces = async () => {
  try {
    const response = await axios.get(
      "https://www.emsifa.com/api-wilayah-indonesia/api/provinces.json"
    );
    provinces.value = response.data;
    console.log("Provinces data:", provinces.value); // Debug log
  } catch (error) {
    console.error("Error fetching provinces:", error);
  }
};

const fetchCities = async (provinceName) => {
  try {
    if (!provinceName) return;
    const selectedProvince = provinces.value.find(
      (province) => province.name === provinceName
    );
    if (!selectedProvince) return;

    const response = await axios.get(
      `https://www.emsifa.com/api-wilayah-indonesia/api/regencies/${selectedProvince.id}.json`
    );
    cities.value = response.data;
    console.log("Cities data:", cities.value); // Debug log
  } catch (error) {
    console.error("Error fetching cities:", error);
  }
};


const filteredCards = computed(() => {
  return cards.value.filter((card) => {
    // Pastikan filter untuk province dan city sesuai dengan data API
    const matchesProvince = !selectedProvince.value || card.province.toLowerCase() === selectedProvince.value.toLowerCase();
    const matchesCity = !selectedCity.value || card.city.toLowerCase() === selectedCity.value.toLowerCase();
    
    // Pastikan format tanggal di-convert dengan benar
    const matchesDate =
      (!startDate.value || new Date(card.date) >= new Date(startDate.value)) &&
      (!endDate.value || new Date(card.date) <= new Date(endDate.value));

    // Search filter
    const matchesSearch =
      !searchQuery.value ||
      Object.values(card).some((value) =>
        String(value).toLowerCase().includes(searchQuery.value.toLowerCase())
      );

    return matchesProvince && matchesCity && matchesDate && matchesSearch;
  });
});



const applyFiltersAndClose = () => {
  showFilterModal.value = false;
};

const clearFilters = () => {
  selectedProvince.value = "";
  selectedCity.value = "";
  startDate.value = "";
  endDate.value = "";
  searchQuery.value = "";
};

onMounted(() => {
  fetchConcerts();
  fetchProvinces();
  isVisible.value = true;
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

.card {
  height: 350px; /* Tetapkan tinggi tetap */
}

.card figure img {
  object-fit: cover; /* Pastikan gambar sesuai */
  height: 100%; /* Isi penuh tinggi */
  width: 100%; /* Isi penuh lebar */
}

/* Skeleton Loader Styles */
.skeleton-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px;
  background-color: #f3f4f6;
  height: 100%;
}

.skeleton-image {
  background: #e0e0e0;
  height: 180px;
  border-radius: 8px;
}

.skeleton-text {
  background: #e0e0e0;
  height: 20px;
  margin-top: 10px;
  border-radius: 4px;
  width: 70%;
}
</style>
