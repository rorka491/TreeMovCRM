import { JSX, ReactElement } from 'react'
import { Navigate } from 'react-router-dom'

interface ProtectedRouteProps {
  children: ReactElement
}

export const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const token = localStorage.getItem('accessToken')
  if (!token) {
    return <Navigate to="/login" replace />
  } else {
      return children
  }
}




