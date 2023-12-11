import './Home.scss'
import TabBar from '../../components/TabBar.tsx'

const Home = () => {
	window.location.href = '/games'

	return (
		<TabBar />
		// 一些炫酷且通用的首页元素
	)
}

export default Home
