import express from 'express'
import { 
  getPapers, 
  getPaper, 
  createPaper, 
  updatePaper, 
  deletePaper,
  searchPapers 
} from '../controllers/paper.controller.js'
import { protect } from '../middleware/auth.middleware.js'

const router = express.Router()

router.get('/search', searchPapers)
router.get('/', getPapers)
router.get('/:id', getPaper)
router.post('/', protect, createPaper)
router.put('/:id', protect, updatePaper)
router.delete('/:id', protect, deletePaper)

export default router

