<template>
    <div class="login-container">
        <div class="login-header">
            Welcome to Travis's Kanban Board!
            <div class="login-subtitle">
                Please log in to continue
            </div>
        </div>
        <div class="login-form">
            <form @submit.prevent="handleLogin">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" v-model="username" required />
                </div>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" v-model="password" required />
                </div>
                <button class="login-button" type="submit">Login</button>
            </form>
            <div v-if="props.errorMessage" class="error-message">
                {{ props.errorMessage }}
            </div>
        </div>
    </div>

</template>

<script setup lang="ts">
import { ref, defineEmits } from 'vue'

const username = ref('')
const password = ref('')

const emit = defineEmits<{
  (e: 'login', payload: { username: string; password: string }): void
}>()

const props = defineProps<{
    errorMessage?: string
}>();

function handleLogin() {
    emit('login', {
        username: username.value,
        password: password.value
    });
}
</script>