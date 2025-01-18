<template>
  <MainLayout>
    <div class="max-w-md mx-auto bg-white shadow-lg rounded-lg overflow-hidden p-4 mt-6">
      <h2 class="text-2xl font-bold text-center mb-4">Confirm Payment</h2>

      <!-- Concert Info (Event Info) -->
      <div class="border-b pb-4 mb-4">
        <h3 class="text-lg font-semibold">Event Info</h3>
        <p class="text-gray-500">Title: {{ eventInfo.title }}</p>
        <p class="text-gray-500">Date: {{ eventInfo.date }}</p>
        <p class="text-gray-500">Location: {{ eventInfo.location }}</p>
        <p class="text-gray-500">Time: {{ eventInfo.time }}</p>
        <p class="text-gray-900 font-bold mt-2">Price: Rp. {{ formattedPrice }}</p>
      </div>

      <!-- Ticket Info -->
      <div class="border-b pb-4 mb-4">
        <h3 class="text-lg font-semibold">Ticket Info</h3>
        <p class="text-gray-500">Event: {{ eventInfo.title }}</p>
        <p class="text-gray-500">Price: Rp. {{ formattedPrice }} / ticket</p>
        <p class="text-gray-500">Quantity: {{ ticketInfo.quantity }}</p>
        <p class="text-gray-900 font-bold mt-2">Total: Rp. {{ totalCost }}</p>
      </div>

      <!-- Payment Method -->
      <div class="pb-4">
        <h3 class="text-lg font-semibold mb-2">Payment Method</h3>
        <select
          v-model="selectedPaymentMethod"
          class="w-full border border-gray-300 rounded-lg p-2 text-gray-700"
        >
          <option disabled value="">Select a payment method</option>
          <optgroup label="Transfer Bank">
            <option
              v-for="(bank, index) in paymentMethods.banks"
              :key="index"
              :value="bank.name"
            >
              <img
                :src="bank.logo"
                alt="Bank Logo"
                class="inline-block w-6 h-6 mr-2 align-middle"
              />
              {{ bank.name }}
            </option>
          </optgroup>
          <optgroup label="E-Wallet">
            <option
              v-for="(wallet, index) in paymentMethods.wallets"
              :key="index"
              :value="wallet.name"
            >
              <img
                :src="wallet.logo"
                alt="E-Wallet Logo"
                class="inline-block w-6 h-6 mr-2 align-middle"
              />
              {{ wallet.name }}
            </option>
          </optgroup>
        </select>
      </div>

      <!-- Confirm Payment Button -->
      <button
        @click="showModal = true"
        :disabled="!selectedPaymentMethod"
        class="mt-6 w-full bg-green-500 text-white text-lg font-bold py-2 rounded-lg hover:bg-green-600"
      >
        Confirm Payment
      </button>
    </div>

    <!-- Modal for Confirmation -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg shadow-lg w-80">
        <h3 class="text-xl font-semibold mb-4">Confirm Payment</h3>
        <p>Are you sure you want to confirm payment?</p>
        <div class="mt-4 flex justify-between">
          <button
            @click="confirmPayment"
            class="bg-green-500 text-white py-2 px-4 rounded-lg hover:bg-green-600"
          >
            Yes
          </button>
          <button
            @click="showModal = false"
            class="bg-red-500 text-white py-2 px-4 rounded-lg hover:bg-red-600"
          >
            No
          </button>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import MainLayout from "@/layouts/MainLayout.vue";
import { ref, computed } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();

// State for modal visibility
const showModal = ref(false);

// Get event and ticket data
const eventInfo = JSON.parse(localStorage.getItem("selectedCard")) || {};
const ticketInfo = JSON.parse(localStorage.getItem("ticketInfo")) || {};

// User data
const userId = localStorage.getItem("user_id");

// Payment method selection
const selectedPaymentMethod = ref("");

// Payment method options
const paymentMethods = {
  banks: [
    { name: "Bank BNI", logo: "/logos/bni.png" },
    { name: "Bank BRI", logo: "/logos/bri.png" },
    { name: "Bank Mandiri", logo: "/logos/mandiri.png" },
    { name: "Bank BSI", logo: "/logos/bsi.png" },
    { name: "Bank BJB", logo: "/logos/bjb.png" },
    { name: "SeaBank", logo: "/logos/seabank.png" },
  ],
  wallets: [
    { name: "ShopeePay", logo: "/logos/shopeepay.png" },
    { name: "Dana", logo: "/logos/dana.png" },
    { name: "OVO", logo: "/logos/ovo.png" },
    { name: "GoPay", logo: "/logos/gopay.png" },
  ],
};

// Format price
const formatPrice = (price) => new Intl.NumberFormat("id-ID").format(price);
const formattedPrice = computed(() => formatPrice(eventInfo.price));
const totalCost = computed(() => formatPrice(eventInfo.price * ticketInfo.quantity));

// Handle payment confirmation
const confirmPayment = async () => {
  try {
    const transactionData = {
      user_id: userId,
      concert_id: eventInfo._id,
      payment_method: selectedPaymentMethod.value,
      quantity: ticketInfo.quantity,
      total_cost: eventInfo.price * ticketInfo.quantity,
    };

    // Call API to create transaction
    const response = await axios.post("http://127.0.0.1:5000/api/transaction", transactionData);
    
    if (response.data.status === "success") {
      alert("Payment confirmed!");
      router.push("/success");
    }
  } catch (error) {
    console.error("Error confirming payment:", error);
  }
};
</script>

<style scoped>
/* Add custom styling for modal */
</style>
