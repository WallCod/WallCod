/**
 * TypeScript type definitions
 */

export interface User {
  id: number
  email: string
  username: string
  full_name?: string
  bio?: string
  avatar_url?: string
  github_url?: string
  linkedin_url?: string
  twitter_url?: string
  website_url?: string
  job_title?: string
  company?: string
  location?: string
  is_active: boolean
  created_at: string
}

export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  email: string
  username: string
  password: string
  full_name?: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface ApiError {
  detail: string | { msg: string; type: string }[]
}

export interface Project {
  id: number
  title: string
  description: string
  technologies: string[]
  github_url?: string
  demo_url?: string
  image_url?: string
  created_at: string
}

export interface Skill {
  name: string
  category: 'frontend' | 'backend' | 'database' | 'tools' | 'security'
  level: 'beginner' | 'intermediate' | 'advanced' | 'expert'
  icon?: string
}

export interface Experience {
  id: number
  company: string
  position: string
  description: string
  start_date: string
  end_date?: string
  current: boolean
}

export interface BlogPost {
  id: number
  title: string
  slug: string
  content: string
  excerpt: string
  tags: string[]
  published: boolean
  created_at: string
  updated_at: string
}
