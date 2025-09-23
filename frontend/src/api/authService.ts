import apiClient from './api_client'

export async function login(username:string, password:string): Promise<boolean> {
    try {
        const response = await apiClient.post('/token/', { username, password })
        const access_token = response.data.access
        const refresh_token = response.data.refresh
        localStorage.setItem('accessToken', access_token)
        localStorage.setItem('refeshToken', refresh_token)
        return true
    } catch (error) {
        console.error('Ошибка логина', error)
        return false
    }
}


export async function logout(): Promise<boolean> {
    try{
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        return true
    } catch (error) {
        console.error('Ошибка выхода', error)
        return false
    }
}