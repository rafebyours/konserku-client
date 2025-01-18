<template>
    <div>
      <!-- Konten Utama -->
      <div class="max-w-md mx-auto bg-white shadow-lg rounded-lg overflow-hidden p-4 mt-6">
        <h2 class="text-2xl font-bold text-center mb-4">Confirm Payment</h2>
  
        <!-- Ticket Info -->
        <div class="border-b pb-4 mb-4">
          <h3 class="text-lg font-semibold">Ticket Info</h3>
          <p class="text-gray-500">Event: {{ ticketInfo.title }}</p>
          <p class="text-gray-500">Price: Rp. {{ formattedPrice }} / ticket</p>
          <p class="text-gray-500">Quantity: {{ ticketInfo.quantity }}</p>
          <p class="text-gray-900 font-bold mt-2">Total: Rp. {{ totalCost }}</p>
        </div>
  
        <!-- User Info -->
        <div class="border-b pb-4 mb-4">
          <h3 class="text-lg font-semibold">User Info</h3>
          <p class="text-gray-500">Name: {{ userInfo.name }}</p>
          <p class="text-gray-500">Email: {{ userInfo.email }}</p>
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
                {{ bank.name }}
              </option>
            </optgroup>
            <optgroup label="E-Wallet">
              <option
                v-for="(wallet, index) in paymentMethods.wallets"
                :key="index"
                :value="wallet.name"
              >
                {{ wallet.name }}
              </option>
            </optgroup>
          </select>
        </div>
  
        <!-- Confirm Payment Button -->
        <button
          @click="confirmPayment"
          :disabled="!selectedPaymentMethod"
          class="mt-6 w-full bg-green-500 text-white text-lg font-bold py-2 rounded-lg hover:bg-green-600"
        >
          Confirm Payment
        </button>
      </div>
  
      <!-- Modal -->
      <div
        v-if="showModal"
        class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50"
      >
        <div class="bg-white rounded-lg p-6 shadow-lg w-96">
          <h2 class="text-lg font-bold mb-4">Transaksi Berhasil</h2>
          <p class="text-gray-600 mb-4">
            {{ paymentStatusMessage }}
          </p>
          <button
            @click="redirectToNextStep"
            class="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600"
          >
            {{ nextStepLabel }}
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from "vue";
  import { useRouter } from "vue-router";
  import axios from "axios";
  
  const router = useRouter();
  
  // Data transaksi dari localStorage
  const ticketInfo = JSON.parse(localStorage.getItem("ticketInfo")) || {
    title: "Unknown Event",
    price: 0,
    quantity: 0,
  };
  
  const userId = localStorage.getItem("user_id");
  const selectedCard = JSON.parse(localStorage.getItem("selectedCard"));
  const concert_id = selectedCard ? selectedCard._id : null;
  
  if (!concert_id) {
    console.error("Concert ID not found in localStorage");
  }
  
  // User Info
  const userInfo = ref({});
  const fetchUserInfo = async () => {
    try {
      const response = await axios.get(
        `https://api-ticketconcert.vercel.app/api/user-profile/${userId}`
      );
      userInfo.value = response.data;
    } catch (error) {
      console.error("Error fetching user info:", error);
    }
  };
  
  // Payment Methods
  const paymentMethods = {
    banks: [
      { name: "Bank BNI" },
      { name: "Bank BRI" },
      { name: "Bank Mandiri" },
      { name: "Bank BSI" },
    ],
    wallets: [
      { name: "ShopeePay" },
      { name: "Dana" },
      { name: "OVO" },
      { name: "GoPay" },
    ],
  };
  
  const selectedPaymentMethod = ref("");
  const showModal = ref(false); // Modal state
  const statusPayment = ref(0); // Default status pembayaran
  
  // Format harga
  const formatPrice = (price) => new Intl.NumberFormat("id-ID").format(price);
  const formattedPrice = computed(() => formatPrice(ticketInfo.price));
  const totalCost = computed(() =>
    formatPrice(ticketInfo.price * ticketInfo.quantity)
  );
  
  // Pesan modal
  const paymentStatusMessage = computed(() => {
    return statusPayment.value === 1
      ? "Pembayaran Anda telah selesai. Tiket elektronik akan segera dikirim."
      : "Transaksi berhasil dibuat. Silakan lakukan pembayaran untuk menyelesaikan proses pembelian.";
  });
  
  // Tombol langkah berikutnya
  const nextStepLabel = computed(() => {
    return statusPayment.value === 1 ? "Lihat Tiket" : "Lanjutkan Pembayaran";
  });
  
  // Arahkan ke langkah berikutnya
  const redirectToNextStep = () => {
    if (statusPayment.value === 1) {
      router.push("/myticket");
    } else {
      // Arahkan ke halaman instruksi pembayaran
      router.push("/myticket");
    }
  };
  
  // Konfirmasi pembayaran
  const confirmPayment = async () => {
    try {
      if (!concert_id) {
        alert("Concert ID is missing. Please try again.");
        return;
      }
  
      if (!selectedPaymentMethod.value) {
        alert("Please select a payment method.");
        return;
      }
  
      const transactionData = {
        user_id: userId,
        concert_id: concert_id, // Pastikan concert_id tersedia
        payment_method: selectedPaymentMethod.value,
        quantity: ticketInfo.quantity,
        total_cost: ticketInfo.price * ticketInfo.quantity,
      };
  
      const response = await axios.post(
        "https://api-ticketconcert.vercel.app/api/transaction",
        transactionData
      );
  
      if (response.data.status === "success") {
        showModal.value = true; // Tampilkan modal setelah transaksi berhasil
        statusPayment.value = 0; // Tentukan status jika pembayaran belum selesai
      } else {
        alert(`Error: ${response.data.message}`);
      }
    } catch (error) {
      console.error("Transaction Error:", error.response || error.message);
      if (error.response) {
        alert(`Error: ${error.response.data.message || "An unexpected error occurred."}`);
      } else {
        alert("An error occurred while creating the transaction.");
      }
    }
  };
  
  // Fetch user info saat komponen di-mount
  fetchUserInfo();
  </script>
  
  <style>
  /* Gaya untuk modal */
  </style>
  