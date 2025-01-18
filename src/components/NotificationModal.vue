<template>
    <transition name="fade">
      <div v-if="showModal" class="modal-overlay">
        <div class="modal">
          <div class="modal-content">
            <p>{{ message }}</p> <!-- Menampilkan message yang diteruskan -->
          </div>
        </div>
      </div>
    </transition>
  </template>
  
  <script>
  export default {
    props: {
      showModal: {
        type: Boolean,
        required: true,
      },
      message: {
        type: String,
        required: true,
      },
    },
    watch: {
      showModal(newValue) {
        if (newValue) {
          setTimeout(() => {
            this.$emit('closeModal'); // Emit event untuk menutup modal
          }, 3000); // Menutup modal setelah 3 detik
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Overlay Styling */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
  }
  
  /* Modal Styling */
  .modal {
    background-color: #333;
    color: white;
    padding: 15px 30px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    max-width: 400px;
    width: 100%;
    text-align: center;
  }
  
  .modal-content {
    font-size: 16px;
  }
  
  /* Animasi Fade */
  @keyframes fadeOut {
    from {
      opacity: 1;
    }
    to {
      opacity: 0;
    }
  }
  
  .fade-enter-active, .fade-leave-active {
    transition: opacity 0.5s ease;
  }
  
  .fade-enter, .fade-leave-to {
    opacity: 0;
  }
  </style>
  