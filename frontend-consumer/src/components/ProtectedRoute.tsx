import React, { useEffect } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { getCurrentUser } from '../api/auth'
import { Spin } from 'antd'

interface ProtectedRouteProps {
  children: React.ReactNode
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated, user, setUser, clearAuth } = useAuthStore()
  const [loading, setLoading] = React.useState(true)

  useEffect(() => {
    const checkAuth = async () => {
      if (isAuthenticated && !user) {
        try {
          const userData = await getCurrentUser()
          setUser(userData)
        } catch (error) {
          clearAuth()
        } finally {
          setLoading(false)
        }
      } else {
        setLoading(false)
      }
    }

    checkAuth()
  }, [isAuthenticated, user, setUser, clearAuth])

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh'
      }}>
        <Spin size="large" tip="加载中..." />
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return <>{children}</>
}

export default ProtectedRoute
