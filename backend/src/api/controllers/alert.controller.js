import { Alert } from '../../models/Alert.model.js'
import { logger } from '../../utils/logger.js'

export const getAlerts = async (req, res) => {
  try {
    const alerts = await Alert.find({ user: req.user.id })

    res.status(200).json({
      success: true,
      count: alerts.length,
      data: alerts
    })
  } catch (error) {
    logger.error(`Get alerts error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

export const getAlert = async (req, res) => {
  try {
    const alert = await Alert.findOne({
      _id: req.params.id,
      user: req.user.id
    })

    if (!alert) {
      return res.status(404).json({
        success: false,
        error: 'Alert not found'
      })
    }

    res.status(200).json({
      success: true,
      data: alert
    })
  } catch (error) {
    logger.error(`Get alert error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

export const createAlert = async (req, res) => {
  try {
    const alert = await Alert.create({
      ...req.body,
      user: req.user.id
    })

    res.status(201).json({
      success: true,
      data: alert
    })
  } catch (error) {
    logger.error(`Create alert error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

export const updateAlert = async (req, res) => {
  try {
    const alert = await Alert.findOneAndUpdate(
      { _id: req.params.id, user: req.user.id },
      req.body,
      {
        new: true,
        runValidators: true
      }
    )

    if (!alert) {
      return res.status(404).json({
        success: false,
        error: 'Alert not found'
      })
    }

    res.status(200).json({
      success: true,
      data: alert
    })
  } catch (error) {
    logger.error(`Update alert error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

export const markAsRead = async (req, res) => {
  try {
    const alert = await Alert.findOneAndUpdate(
      { _id: req.params.id, user: req.user.id },
      { read: true },
      { new: true }
    )

    if (!alert) {
      return res.status(404).json({
        success: false,
        error: 'Alert not found'
      })
    }

    res.status(200).json({
      success: true,
      data: alert
    })
  } catch (error) {
    logger.error(`Mark as read error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

export const deleteAlert = async (req, res) => {
  try {
    const alert = await Alert.findOne({
      _id: req.params.id,
      user: req.user.id
    })

    if (!alert) {
      return res.status(404).json({
        success: false,
        error: 'Alert not found'
      })
    }

    await alert.deleteOne()

    res.status(200).json({
      success: true,
      data: {}
    })
  } catch (error) {
    logger.error(`Delete alert error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

