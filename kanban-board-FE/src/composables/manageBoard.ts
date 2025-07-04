import { Ref, ref } from 'vue'
import { ColumnType } from '../types/Column'
import { getTasks, login } from '../api/api'

export function manageBoard(columns: Ref<ColumnType[]>) {
    const loggedIn = ref(false)
    const errorMessage = ref('')

    const colorMap = {
        1: 'column-blue',
        2: 'column-yellow',
        3: 'column-red',
    }

    // Load Board Function
    async function loadBoard() {
    try {
        const response = await getTasks()
        columns.value = response.data
        // Assign color classes to each column
        columns.value.forEach((column) => {
        column.colorClass = colorMap[column.id as keyof typeof colorMap]
        })
    } catch (error) {
        console.error('Error fetching tasks:', error)
    }
    }

    // Login Function
    async function handleLogin(payload: { username: string; password: string }) {
    try {
        await login(payload.username, payload.password)
        loggedIn.value = true
        errorMessage.value = ''
        // Load the board after successful login
        await loadBoard()
    } catch (error) {
        console.error('Login failed:', error)
        errorMessage.value = 'Invalid username or password'
        console.error('Error message:', errorMessage.value)
    }
    }

    async function handleLogout() {
    loggedIn.value = false
    }

    return {
        loggedIn,
        errorMessage,
        loadBoard,
        handleLogin,
        handleLogout,
    }
}