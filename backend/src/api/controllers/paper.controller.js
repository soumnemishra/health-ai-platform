import { Paper } from '../../models/Paper.model.js'
import { logger } from '../../utils/logger.js'

export const getPapers = async (req, res) => {
  try {
    const papers = await Paper.find()

    res.status(200).json({
      success: true,
      count: papers.length,
      data: papers
    })
  } catch (error) {
    logger.error(`Get papers error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

export const getPaper = async (req, res) => {
  try {
    const paper = await Paper.findById(req.params.id)

    if (!paper) {
      return res.status(404).json({
        success: false,
        error: 'Paper not found'
      })
    }

    res.status(200).json({
      success: true,
      data: paper
    })
  } catch (error) {
    logger.error(`Get paper error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

export const createPaper = async (req, res) => {
  try {
    const paper = await Paper.create(req.body)

    res.status(201).json({
      success: true,
      data: paper
    })
  } catch (error) {
    logger.error(`Create paper error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

export const updatePaper = async (req, res) => {
  try {
    const paper = await Paper.findByIdAndUpdate(
      req.params.id,
      req.body,
      {
        new: true,
        runValidators: true
      }
    )

    if (!paper) {
      return res.status(404).json({
        success: false,
        error: 'Paper not found'
      })
    }

    res.status(200).json({
      success: true,
      data: paper
    })
  } catch (error) {
    logger.error(`Update paper error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

export const deletePaper = async (req, res) => {
  try {
    const paper = await Paper.findById(req.params.id)

    if (!paper) {
      return res.status(404).json({
        success: false,
        error: 'Paper not found'
      })
    }

    await paper.deleteOne()

    res.status(200).json({
      success: true,
      data: {}
    })
  } catch (error) {
    logger.error(`Delete paper error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

export const searchPapers = async (req, res) => {
  try {
    const { query, limit = 10 } = req.query

    const papers = await Paper.find({
      $or: [
        { title: { $regex: query, $options: 'i' } },
        { abstract: { $regex: query, $options: 'i' } },
        { keywords: { $in: [new RegExp(query, 'i')] } }
      ]
    }).limit(parseInt(limit))

    res.status(200).json({
      success: true,
      count: papers.length,
      data: papers
    })
  } catch (error) {
    logger.error(`Search papers error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
}

