import { User } from '../../models/User.model.js'
import { logger } from '../../utils/logger.js'

export const getUsers = async (req, res) => {
  try {
    const users = await User.find().select('-password')

    res.status(200).json({
      success: true,
      count: users.length,
      data: users
    })
  } catch (error) {
    logger.error(`Get users error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

export const getUser = async (req, res) => {
  try {
    const user = await User.findById(req.params.id).select('-password')

    if (!user) {
      return res.status(404).json({
        success: false,
        error: 'User not found'
      })
    }

    res.status(200).json({
      success: true,
      data: user
    })
  } catch (error) {
    logger.error(`Get user error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

export const updateUser = async (req, res) => {
  try {
    const user = await User.findByIdAndUpdate(
      req.params.id,
      req.body,
      {
        new: true,
        runValidators: true
      }
    ).select('-password')

    if (!user) {
      return res.status(404).json({
        success: false,
        error: 'User not found'
      })
    }

    res.status(200).json({
      success: true,
      data: user
    })
  } catch (error) {
    logger.error(`Update user error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

export const deleteUser = async (req, res) => {
  try {
    const user = await User.findById(req.params.id)

    if (!user) {
      return res.status(404).json({
        success: false,
        error: 'User not found'
      })
    }

    await user.deleteOne()

    res.status(200).json({
      success: true,
      data: {}
    })
  } catch (error) {
    logger.error(`Delete user error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

