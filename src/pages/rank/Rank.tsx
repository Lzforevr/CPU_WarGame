import './Rank.scss'
import TabBar from '../../components/TabBar.tsx'
import { List, Button, Spin, Space } from '@douyinfe/semi-ui'
import InfiniteScroll from 'react-infinite-scroller'
import { useEffect, useState } from 'react'
import { UserOnRank, getRankDTO } from '../../data/types.tsx'
import { Axios } from '../../tool/tool.tsx'
import exampleRank from '../../data/exampleRank.json'
import { Trophy } from '@icon-park/react'
import { Window } from '../../components/Window.tsx'

function Rank() {
	const [loading, setLoading] = useState(false)
	const [hasMore, setHasMore] = useState(true)
	const [showLoadMore, setShowLoadMore] = useState(false)
	const [fullData, setFullData] = useState<UserOnRank[]>(exampleRank)
	const [dataSource, setDataSource] = useState<UserOnRank[]>([])

	useEffect(() => {
		setLoading(true)
		Axios.get<getRankDTO>('/leaderboard')
			.then(res => {
				setFullData(res.data.data)
				// setDataSource(res.data.data)
				console.log(res.data.data)
			})
			.then(() => {
				setLoading(false)
				setShowLoadMore(true)
			})
	}, [])

	const fetchData = async () => {
		setLoading(true)
		setTimeout(() => {
			console.log(fullData)
			const data = fullData.slice(0, dataSource.length + 10)
			setDataSource(data)
			setLoading(false)
			if (data.length >= fullData.length) {
				setHasMore(false)
			}
			setShowLoadMore(true)
		}, 500)
	}

	const loadMore =
		!loading && hasMore && showLoadMore ? (
			<div
				style={{
					textAlign: 'center',
					height: 32,
					lineHeight: '32px'
				}}>
				<Button onClick={fetchData}>显示更多</Button>
			</div>
		) : null

	return (
		<div className='rank'>
			<TabBar />
			<InfiniteScroll
				initialLoad={true}
				pageStart={0}
				threshold={40}
				loadMore={fetchData}
				hasMore={!loading && hasMore && !showLoadMore}
				useWindow={true}>
				<Window>
					<List
						style={{
							width: '40%',
							backgroundColor: 'var(--semi-color-fill-0)',
							padding: '0 20px 20px 20px',
							margin: '20px 0',
							borderRadius: '10px'
						}}
						loadMore={loadMore}
						dataSource={dataSource}
						header={
							<h1 style={{ textAlign: 'center' }}>
								<span style={{ color: 'var(--semi-color-text-0)' }}>
									排行榜
								</span>
							</h1>
						}
						renderItem={item => (
							<List.Item
								header={
									item.id === 1 ? (
										<Trophy
											theme='two-tone'
											size='35'
											fill={['#f5a623', '#f8e71c']}
										/>
									) : item.id === 2 ? (
										<Trophy
											theme='two-tone'
											size='30'
											fill={['#9b9b9b', '#c5c5c5']}
										/>
									) : item.id === 3 ? (
										<Trophy
											theme='two-tone'
											size='24'
											fill={['#4a4a4a', '#8b572a']}
										/>
									) : (
										<span style={{ color: 'var(--semi-color-text-2)' }}>
											{item.id}
										</span>
									)
								}
								main={
									<div>
										<span
											style={{
												color: 'var(--semi-color-text-0)',
												fontWeight: 500
											}}>
											{item.name}
										</span>
										<p
											style={{
												color: 'var(--semi-color-text-2)',
												margin: '4px 0'
											}}>
											{item.score}
										</p>
									</div>
								}
								align='center'
							/>
						)}
					/>
					{loading && hasMore && (
						<div style={{ textAlign: 'center' }}>
							<Spin />
						</div>
					)}
				</Window>
			</InfiniteScroll>
		</div>
	)
}

export default Rank
