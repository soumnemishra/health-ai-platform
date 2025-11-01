import { useUser } from '../context/UserContext'
import apiClient from '../api/client'

export function useAuth() {
  const { user, login, logout } = useUser()

  const signIn = async (credentials) => {
    try {
      const response = await apiClient.post('/auth/login', credentials)
      const { user: userData, token } = response.data
      
      localStorage.setItem('authToken', token)
      login(userData)
      
      return { success: true, user: userData }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.message || 'Login failed'
      }
    }
  }

  const signOut = () => {
    logout()
  }

  const isAuthenticated = !!user

  return {
    user,
    isAuthenticated,
    signIn,
    signOut
  }
}

