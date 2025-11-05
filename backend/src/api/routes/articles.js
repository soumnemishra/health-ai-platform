import express from 'express'
import { supabase } from '../../db/supabase.js'
import { logger } from '../../utils/logger.js'

const router = express.Router()

// GET / - Read all articles from raw_articles table
router.get('/', async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('raw_articles')
      .select('*')

    if (error) {
      logger.error(`Get articles error: ${error.message}`)
      return res.status(500).json({
        success: false,
        error: error.message
      })
    }

    res.status(200).json({
      success: true,
      count: data?.length || 0,
      data: data || []
    })
  } catch (error) {
    logger.error(`Get articles error: ${error.message}`)
    res.status(500).json({
      success: false,
      error: 'Server error'
    })
  }
})

export default router
