<template>
  <MainLayout>
    <transition name="fade" @before-enter="beforeEnter" @enter="enter" @leave="leave">
      <div class="container">
        <!-- Header -->
        <div class="header">
          <div class="back-button">
            <button @click="$router.push('/home')">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M15 18L9 12L15 6" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
            </button>
          </div>
          <div class="title font-sans2">My Tickets</div>
        </div>

        <!-- Payment Section -->
        <div class="payment-section">
          <div class="payment-title font-sans">List Ticket</div>
          <div class="tickets-section">
            <!-- Skeleton Loader -->
            <div v-if="transactions.length === 0">
              <div class="skeleton-card" v-for="i in 3" :key="i">
                <div class="skeleton skeleton-title"></div>
                <div class="skeleton skeleton-text"></div>
                <div class="skeleton skeleton-text"></div>
                <div class="skeleton skeleton-text"></div>
              </div>
            </div>

            <!-- Loop through each filtered transaction -->
            <div v-else>
              <div v-for="transaction in filteredTransactions" :key="transaction._id" class="ticket-info">
                <div class="ticket-details">
                  <h2 class="text-1xl font-blackExtended mt-3">
                    <span class="bg-green-100 px-2 py-1 rounded">{{ transaction.concert_details.title }}</span>
                  </h2>
                  <p>{{ transaction.concert_details.location }}</p>
                  <p>{{ transaction.concert_details.date }}</p>
                  <p>Total Ticket: {{ transaction.quantity }}</p>
                  <p>Total: Rp. {{ formatPrice(transaction.total_cost) }}</p>
                </div>

                <!-- Status Payment Badge -->
                <div v-if="transaction.status_payment === 0" class="payment-status-badge">
                  <span class="badge">Belum Dibayar</span>
                </div>
                <div v-else class="payment-status-badge">
                  <span class="badge paid">Sudah Dibayar</span>
                </div>

                <!-- Action Buttons -->
                <div class="details-button">
                  <button
                    v-if="transaction.status_payment === 0"
                    @click="$router.push({ name: 'PaymentPage', params: { id: transaction._id } })"
                    class="view-details-button"
                  >
                    Lakukan Pembayaran
                  </button>
                  <button
                    v-else
                    @click="$router.push({ name: 'eTicket', params: { id: transaction._id } })"
                    class="view-details-button"
                  >
                    Lihat Tiket
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </MainLayout>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import MainLayout from "@/layouts/MainLayout.vue";
import axios from "axios";

// State untuk transaksi
const transactions = ref([]);

// Ambil user_id dari localStorage
const userId = localStorage.getItem("user_id");

// Fungsi untuk memformat harga
const formatPrice = (price) => {
  return new Intl.NumberFormat("id-ID", { style: "currency", currency: "IDR" })
    .format(price)
    .slice(3); // Menghapus simbol mata uang (Rp)
};

// Filter transaksi berdasarkan user_id
const filteredTransactions = computed(() =>
  transactions.value.filter((transaction) => transaction.user_id === userId)
);

// Fetch data transaksi saat komponen dimuat
onMounted(async () => {
  try {
    const response = await axios.get(`https://api-ticketconcert.vercel.app/api/transactions/${userId}`);
    transactions.value = response.data.data;
  } catch (error) {
    console.error("Gagal mengambil data transaksi:", error);
  }
});
</script>

<style scoped>
.container {
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.back-button {
  cursor: pointer;
}

.title {
  font-size: 24px;
  font-weight: bold;
}

.payment-section {
  margin-top: 20px;
}

.payment-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
}

.tickets-section {
  margin-top: 10px;
}

.ticket-info {
  display: flex;
  flex-direction: column;
  position: relative;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.ticket-details {
  flex: 1;
}

.payment-status-badge {
  margin-top: 10px;
}

.badge {
  background-color: red;
  color: white;
  padding: 5px 10px;
  border-radius: 3px;
  font-size: 12px;
}

.badge.paid {
  background-color: green;
}

.details-button {
  margin-top: auto;
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
}

.view-details-button {
  background-color: black;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
}

.view-details-button:hover {
  background-color: #0056b3;
}

.total-price {
  margin-top: 20px;
  font-size: 18px;
  font-weight: bold;
}

/* Skeleton Loader Styles */
.skeleton-card {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
  background-color: #f0f0f0;
  display: flex;
  flex-direction: column;
}

.skeleton {
  background-color: #ccc;
  border-radius: 4px;
  margin-bottom: 8px;
}

.skeleton-title {
  width: 80%;
  height: 20px;
}

.skeleton-text {
  width: 60%;
  height: 15px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
