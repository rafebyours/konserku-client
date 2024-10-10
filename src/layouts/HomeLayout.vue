<template>
    <section>
        <Header />
        <main class="mt-20">
            <slot />
        </main>
        <Footer />
    </section>
</template>

<script setup>
import Header from "@/components/header/index.vue"
import Footer from "@/components/footer/index.vue"
</script>

<style lang="scss" scoped>

</style>