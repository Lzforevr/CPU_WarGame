import axios from 'axios'
import { serverUrl } from '../data/constants'

export const Axios = axios.create({
	baseURL: serverUrl,
	timeout: 10000,
	headers: {
		'Content-Type': 'application/json;charset=UTF-8'
	}
})
