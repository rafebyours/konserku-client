<template>
  <MainLayout>
    <transition name="fade" @before-enter="beforeEnter" @enter="enter" @leave="leave">
      
      <div class="flex flex-col items-center justify-center min-h-screen bg-white">
        <h2 class="text-lg font-blackExtended text-gray-800">Ticket Details</h2>
        <!-- Ticket Container -->
        <div v-if="transaction" class="w-80 bg-white rounded-2xl overflow-hidden mt-4 shadow-xl">
          <!-- Header Section with Back Button -->
        
          <!-- Ticket Image and Title -->
          <div class="relative">
            <img
              :src="transaction.selectedCard.image || 'https://via.placeholder.com/400x200?text=Concert+Image'"
              class="w-full h-40 object-cover"
            />
            <div class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
              <h2 class="text-white text-lg text-center font-blackExtended">
                {{ transaction.selectedCard.title || "Concert Title" }}
              </h2>
            </div>
          </div>

          <!-- Event Details Section -->
          <div class="px-6 py-4">
            <p><strong>Location:</strong> {{ transaction.selectedCard.location }}</p>
            <p><strong>Date & Time:</strong> {{ transaction.selectedCard.date }} at {{ transaction.selectedCard.time }}</p>
            <p><strong>Total Tickets:</strong> {{ transaction.reservationSummary.people }}</p>
            <p><strong>Total Payment:</strong> Rp. {{ formatPrice(transaction.grandTotal) }}</p>

            <div v-if="transaction.paymentMethod === 'credit-card'" class="mt-4">
              <h3 class="font-bold">Payment Method: Credit Card</h3>
              <p>Card Number: {{ transaction.selectedCard.cardNumber }}</p>
              <p>Expiry Date: {{ transaction.selectedCard.expiry }}</p>
              <p>CVC: {{ transaction.selectedCard.cvc }}</p>
            </div>

            <div v-if="transaction.paymentMethod === 'transfer'" class="mt-4">
              <h3 class="font-bold">Payment Method: Transfer</h3>
              <p>Bank: {{ transaction.selectedBank }}</p>
            </div>

            <p><strong>Transaction Date:</strong> {{ transaction.date }}</p>
          </div>

          <!-- Barcode Section -->
          <div class="px-6 py-4 flex justify-center bg-gray-100">
            <img
              src="https://i.pinimg.com/736x/ef/02/9b/ef029b177618ee0dbf95033a08ac0f53.jpg"
              alt="Barcode"
              class="w-full max-w-xs object-contain"
            />
          </div>

          <!-- View My Ticket Button -->
          <div class="px-6 py-4">
            <button
             @click="$router.push('/myticket')"
          class="w-full bg-green-500 text-white py-3 rounded-md font-semibold hover:bg-green-700 transition"
            >
              Lihat Tiket Saya
            </button>
          </div>
        </div>

        <!-- Error Message for Missing Transaction -->
        <div v-else class="error-message text-center">
          <p class="text-red-600 font-bold">Transaction not found.</p>
        </div>
      </div>
    </transition>
  </MainLayout>
</template>

<script setup>
import MainLayout from "@/layouts/MainLayout.vue";
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const transaction = ref(null);

onMounted(() => {
  const transactionId = route.params.id;
  const storedTransactions = JSON.parse(localStorage.getItem('transactions')) || [];
  transaction.value = storedTransactions.find(tx => tx.id === transactionId);
  if (!transaction.value) {
    console.error("Transaction with ID not found.");
  }
});

const formatPrice = (price) => new Intl.NumberFormat('id-ID').format(price);

const beforeEnter = (el) => {
  el.style.opacity = 0;
};

const enter = (el, done) => {
  el.offsetHeight;
  el.style.transition = "opacity 0.5s";
  el.style.opacity = 1;
  done();
};

const leave = (el, done) => {
  el.style.transition = "opacity 0.5s";
  el.style.opacity = 0;
  done();
};

const viewTicket = () => {
  this.$router.push("/myticket");
};
</script>

<style scoped>
.error-message {
  color: red;
  font-weight: bold;
  font-size: 18px;
}
.back-button {
  cursor: pointer;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
</style>
