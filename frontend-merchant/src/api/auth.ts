import client from './client'

export interface RegisterRequest {
  username: string
  phone: string
  password: string
  role: 'merchant' | 'consumer'
  shop_name?: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface UserResponse {
  id: number
  username: string
  phone: string
  role: string
  avatar_url?: string
  status: string
  created_at: string
}

/**
 * 用户注册
 */
export const register = async (data: RegisterRequest): Promise<UserResponse> => {
  const response = await client.post('/api/v1/auth/register', data)
  return response.data
}

/**
 * 用户登录
 */
export const login = async (data: LoginRequest): Promise<TokenResponse> => {
  const response = await client.post('/api/v1/auth/login', data)
  return response.data
}

/**
 * 刷新token
 */
export const refreshToken = async (refreshToken: string): Promise<TokenResponse> => {
  const response = await client.post('/api/v1/auth/refresh', {
    refresh_token: refreshToken,
  })
  return response.data
}

/**
 * 获取当前用户信息
 */
export const getCurrentUser = async (): Promise<UserResponse> => {
  const response = await client.get('/api/v1/auth/me')
  return response.data
}

/**
 * 退出登录
 */
export const logout = async (): Promise<void> => {
  await client.post('/api/v1/auth/logout')
}
