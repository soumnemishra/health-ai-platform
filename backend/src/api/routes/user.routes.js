import express from 'express'
import { getUsers, getUser, updateUser, deleteUser } from '../controllers/user.controller.js'
import { protect } from '../middleware/auth.middleware.js'
import { authorize } from '../middleware/auth.middleware.js'

const router = express.Router()

// All routes require authentication
router.use(protect)

router.get('/', authorize('admin'), getUsers)
router.get('/:id', getUser)
router.put('/:id', updateUser)
router.delete('/:id', authorize('admin'), deleteUser)

export default router

