import bcrypt from 'bcryptjs'
import jwt from 'jsonwebtoken'
import { User } from '../../models/User.model.js'
import { logger } from '../../utils/logger.js'

// Generate JWT Token
const generateToken = (id) => {
  return jwt.sign({ id }, process.env.JWT_SECRET || 'your-secret-key', {
    expiresIn: process.env.JWT_EXPIRE || '7d'
  })
}

export const register = async (req, res) => {
  try {
    const { name, email, password } = req.body

    // Check if user exists
    const userExists = await User.findOne({ email })
    if (userExists) {
      return res.status(400).json({
        success: false,
        error: 'User already exists'
      })
    }

    // Create user
    const user = await User.create({
      name,
      email,
      password
    })

    const token = generateToken(user._id)

    res.status(201).json({
      success: true,
      data: {
        user: {
          id: user._id,
          name: user.name,
          email: user.email
        },
        token
      }
    })
  } catch (error) {
    logger.error(`Register error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

export const login = async (req, res) => {
  try {
    const { email, password } = req.body

    // Validate email & password
    if (!email || !password) {
      return res.status(400).json({
        success: false,
        error: 'Please provide email and password'
      })
    }

    // Check for user
    const user = await User.findOne({ email }).select('+password')
    if (!user) {
      return res.status(401).json({
        success: false,
        error: 'Invalid credentials'
      })
    }

    // Check if password matches
    const isMatch = await user.matchPassword(password)
    if (!isMatch) {
      return res.status(401).json({
        success: false,
        error: 'Invalid credentials'
      })
    }

    const token = generateToken(user._id)

    res.status(200).json({
      success: true,
      data: {
        user: {
          id: user._id,
          name: user.name,
          email: user.email
        },
        token
      }
    })
  } catch (error) {
    logger.error(`Login error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

export const logout = async (req, res) => {
  try {
    res.status(200).json({
      success: true,
      message: 'Logged out successfully'
    })
  } catch (error) {
    logger.error(`Logout error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

export const getMe = async (req, res) => {
  try {
    const user = await User.findById(req.user.id)

    res.status(200).json({
      success: true,
      data: {
        user
      }
    })
  } catch (error) {
    logger.error(`Get me error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

