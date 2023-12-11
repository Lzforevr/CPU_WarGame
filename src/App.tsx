import './App.scss'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import SignUp from './pages/sign-up/SignUp.tsx'
import LogIn from './pages/log-in/LogIn.tsx'
import Games from './pages/games/Games.tsx'
import Rank from './pages/rank/Rank.tsx'
import Library from './pages/library/Library.tsx'

export const App = () => {
	return (
		<BrowserRouter>
			<Routes>
				<Route path='/' element={<Games />} />
				<Route path='/signUp' element={<SignUp />} />
				<Route path='/login' element={<LogIn />} />
				<Route path='/rank' element={<Rank />} />
				<Route path='/library' element={<Library />} />
			</Routes>
		</BrowserRouter>
	)
}
