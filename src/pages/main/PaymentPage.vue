<template>
    <MainLayout>
      <div class="payment-page">
        <div class="header font-blackExtended mt-3">
          <h2>Halaman Pembayaran</h2>
        </div>
  
        <div v-if="transaction" class="transaction-details">
          <div class="ticket-details text font-sans">
            <h3 class="text-1xl font-blackExtended mt-3">Detail Tiket</h3>
            <div class="detail-item">
              <strong>{{ transaction.concert_details.title }}</strong>
            </div>
            <div class="detail-item">
              <strong>Lokasi:</strong>
              <span>{{ transaction.concert_details.location }}</span>
            </div>
            <div class="detail-item">
                <strong>Harga:</strong>
                <span>{{ formatRupiah(transaction.concert_details.price) }}</span>
            </div>
            <div class="detail-item">
              <strong>Jumlah:</strong>
              <span>{{ transaction.quantity }}</span>
            </div>
            <div class="detail-item total">
              <strong>Total Biaya:</strong>
              <span>{{ formatRupiah(transaction.total_cost) }}</span>
            </div>
          </div>
  
          <!-- Payment Method Display -->
          <div class="payment-method">
            <h3>Metode Pembayaran</h3>
            <div class="method-details">
              <p><strong>{{ transaction.payment_method }}</strong></p>
              <p>Nomor Virtual Account: <br>
                <strong>{{ randomAccountNumber }}</strong></p>
              <p>Batas Waktu Pembayaran: <br>
                <strong>{{ countdownTimer }}</strong></p>
            </div>
          </div>
  
         <!-- Payment Button -->
         <div class="payment-actions">
          <button @click="openPaymentModal" class="pay-button">Lakukan Pembayaran</button><br>
          <button @click="openCancelModal" class="cancel-button">Batalkan Transaksi</button>
        </div>
      </div>
    </div>
  
   <!-- Modal for payment confirmation -->
   <div :class="{'modal': true, 'modal-visible': showPaymentModal}" class="modal">
      <div class="modal-content">
        <h3>Apakah Anda yakin ingin melakukan pembayaran?</h3>
        <div class="modal-actions">
          <button @click="closePaymentModal" class="cancel-button">Tidak</button>
          <button @click="confirmPayment" class="confirm-button">Ya</button>
        </div>
      </div>
    </div>
  
  <!-- Modal untuk pembayaran berhasil -->
  <div :class="{'modal': true, 'modal-visible': showSuccessModal}" class="modal">
    <div class="modal-content">
      <div class="modal-success">
      <h3>Pembayaran Berhasil!</h3><br>
      <button @click="redirectToMyTicket" class="close-button">Tutup</button>
    </div>
    </div>
  </div>
  
  <!-- Modal untuk pembatalan transaksi -->
  <div :class="{'modal': true, 'modal-visible': showCancelModal}" class="modal">
    <div class="modal-content">
      <h3>Apakah Anda yakin ingin membatalkan transaksi?</h3>
      <div class="modal-actions">
        <button @click="closeCancelModal" class="cancel-button">Tidak</button>
        <button @click="cancelTransaction" class="confirm-button">Ya</button>
      </div>
    </div>
  </div>

    <!-- Modal untuk pembayaran berhasil -->
    <div :class="{'modal': true, 'modal-visible': showDeleteSucccesModals}" class="modal">
    <div class="modal-content">
      <div class="modal-success">
      <h3>Transaksi Berhasil Dibatalkan!</h3><br>
      <button @click="redirectToMyTicket" class="cancel-button">Tutup</button>
    </div>
    </div>
  </div>
  
  </MainLayout>
  </template>
  
  
  <script setup>
  import { ref, onMounted, computed } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import MainLayout from '@/layouts/MainLayout.vue';
  
  // Declare state variables using ref()
  const transaction = ref(null); // Data transaksi
  const showPaymentModal = ref(false); // Modal for payment confirmation
  const showSuccessModal = ref(false); // Modal for payment success
  const showCancelModal = ref(false); // Modal for cancellation confirmation
  const showDeleteSucccesModals = ref(false);
  const randomAccountNumber = computed(() => {
    return `123-456-78${Math.floor(Math.random() * 1000)}`; // Generate random account number
  });
  const countdownTime = ref(24 * 60 * 60); // 24 hours in seconds
  const countdownTimer = computed(() => {
    const hours = Math.floor(countdownTime.value / 3600);
    const minutes = Math.floor((countdownTime.value % 3600) / 60);
    const seconds = countdownTime.value % 60;
    return `${hours} jam ${minutes} menit ${seconds} detik`;
  });
  
  // Use router and route for navigation
  const route = useRoute();
  const router = useRouter();
  
  // Fetch transaction details from API
  const fetchTransactionDetails = async () => {
    try {
      const transactionId = route.params.id;
      const response = await fetch(`https://api-ticketconcert.vercel.app/api/ticket/${transactionId}`);
      const data = await response.json();
  
      if (data.status === 'success') {
        transaction.value = data.data;
        startCountdown(); // Start countdown timer after fetching transaction details
      } else {
        router.push({ name: 'NotFoundPage' }); // Redirect if transaction not found
      }
    } catch (error) {
      console.error('Error fetching transaction:', error);
      router.push({ name: 'ErrorPage' }); // Redirect on error
    }
  };
  
  // Start countdown timer
  const startCountdown = () => {
    const interval = setInterval(() => {
      if (countdownTime.value > 0) {
        countdownTime.value--;
      } else {
        clearInterval(interval);
      }
    }, 1000); // Update countdown every second
  };
  
  // Handle opening payment confirmation modal
  const openPaymentModal = () => {
    showPaymentModal.value = true; // Open the modal when clicking "Lakukan Pembayaran"
  };
  
  // Method to close payment modal
  const closePaymentModal = () => {
    showPaymentModal.value = false; // Close the modal when clicking "Tidak"
  };
  
  // Handle confirming payment and updating status
  const confirmPayment = async () => {
    try {
      const transactionId = route.params.id; // Ambil transactionId dari params
      const response = await fetch(`https://api-ticketconcert.vercel.app/api/ticket/${transactionId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          status_payment: 1, // Update status_payment ke 1 (berhasil)
        }),
      });
  
      // Periksa status code HTTP untuk memastikan berhasil
      if (response.ok) {
        const data = await response.json();
        if (data.message === 'Transaction updated successfully') {
          // Menampilkan modal sukses langsung setelah pembayaran berhasil
          showPaymentModal.value = false; // Menutup modal pembayaran
          showSuccessModal.value = true; // Menampilkan modal sukses
        } else {
          alert('Terjadi kesalahan saat melakukan pembayaran.');
        }
      } else {
        // Menangani error jika status code bukan 200-299
        alert('Gagal mengonfirmasi pembayaran. Coba lagi.');
      }
    } catch (error) {
      console.error('Error confirming payment:', error);
      alert('Terjadi kesalahan saat melakukan pembayaran.');
    }
  };
  
  // Handle opening cancel modal
  const openCancelModal = () => {
    showCancelModal.value = true; // Show the cancel confirmation modal
  };
  
  // Method to close cancel modal
  const closeCancelModal = () => {
    showCancelModal.value = false; // Close the cancel modal
  };
  
  // Method to cancel the transaction
  const cancelTransaction = async () => {
  try {
    const transactionId = route.params.id;
    const response = await fetch(`https://api-ticketconcert.vercel.app/api/transactions/${transactionId}`, {
      method: 'DELETE', // Assuming an endpoint for deleting the transaction exists
    });

    if (response.ok) {
      // Show a modal indicating that the transaction was successfully deleted
      showPaymentModal.value = false;
      showDeleteSucccesModals.value = true; // Use a modal to show success message
      setTimeout(() => {
        showDeleteSucccesModals.value = false; // Close the modal after a delay (e.g., 2 seconds)
        router.push('/myTicket'); // Redirect to the "My Ticket" page or desired route
      }, 2000); // Modal will show for 2 seconds
    } else {
      alert('Gagal membatalkan transaksi.');
    }
  } catch (error) {
    console.error('Error canceling transaction:', error);
    alert('Terjadi kesalahan saat membatalkan transaksi.');
  }
};

  
  // Format angka ke format Rupiah
  const formatRupiah = (value) => {
    return new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR',
    }).format(value);
  };
  
  // Redirect to "My Tickets" page
  const redirectToMyTicket = () => {
    router.push('/myTicket');
  };
  
  // Fetch transaction details on mount
  onMounted(() => {
    fetchTransactionDetails();
  });
  </script>
  
  
  <style scoped>
  .payment-page {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 8px;
  }
  
  .header {
    text-align: center;
    margin-bottom: 20px;
  }
  
  h2 {
    font-size: 28px;
    color: #333;
    font-weight: bold;
  }
  
  .transaction-details {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .ticket-details {
    margin-bottom: 30px;
  }
  
  .ticket-details h3 {
    font-size: 20px;
    font-weight: bold;
    color: #333;
    margin-bottom: 10px;
  }
  
  .detail-item {
    display: flex;
    justify-content: space-between;
    margin: 10px 0;
  }
  
  .detail-item strong {
    font-weight: bold;
  }
  
  .total {
    border-top: 2px solid #ccc;
    padding-top: 15px;
    margin-top: 20px;
  }
  
  .payment-method {
    margin-bottom: 20px;
  }
  
  .method-details p {
    margin: 5px 0;
  }
  
  .payment-actions {
  display: flex;
  flex-direction: column;
  gap: 1px; /* Adjust the gap between the buttons */
}

  
  .pay-button {
    background-color: #4CAF50;
    color: white;
    padding: 12px 30px;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    border: none;
    border-radius: 8px;
    transition: background-color 0.3s;
  }
  
  .pay-button:hover {
    background-color: #45a049;
  }
  
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    transition: opacity 0.3s ease-in-out;
    opacity: 0;
    pointer-events: none; /* Prevents interaction when hidden */
  }
  
  .modal-visible {
    opacity: 1;
    pointer-events: auto; /* Enables interaction when visible */
  }

  .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
  }
  
  .modal-actions {
    margin-top: 20px;
    display: flex;
  justify-content: center;
  gap: 15px; /* Memberikan jarak 15px antara tombol */
  }

  .modal-success{
    flex-direction: column; /* Susun elemen secara vertikal */
  align-items: center; /* Pusatkan elemen secara horizontal */
  gap: 20px; /* Tambahkan jarak antar elemen */
  }
  
  .confirm-button,
  .cancel-button,
  .showDeleteSucccesModals,
  .close-button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    border: none;
    border-radius: 4px;
  }
  
  .confirm-button {
    background-color: #4CAF50;
    color: white;
  }
  
  .cancel-button {
    background-color: #f44336;
    color: white;
  }
  
  .close-button {
    background-color: #008CBA;
    color: white;
  }
  
  .confirm-button:hover {
    background-color: #45a049;
  }
  
  .cancel-button:hover {
    background-color: #d32f2f;
  }
  
  .close-button:hover {
    background-color: #007bb5;
  }
  </style>
  