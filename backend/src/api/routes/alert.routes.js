import express from 'express'
import { 
  getAlerts, 
  getAlert, 
  createAlert, 
  updateAlert, 
  deleteAlert,
  markAsRead 
} from '../controllers/alert.controller.js'
import { protect } from '../middleware/auth.middleware.js'

const router = express.Router()

// All routes require authentication
router.use(protect)

router.get('/', getAlerts)
router.get('/:id', getAlert)
router.post('/', createAlert)
router.put('/:id', updateAlert)
router.patch('/:id/read', markAsRead)
router.delete('/:id', deleteAlert)

export default router

