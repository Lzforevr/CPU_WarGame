import { Card, Space, Button, Image } from '@douyinfe/semi-ui'

const GameCard = props => {
	const { Meta } = Card
	const exampleImgUrl =
		'https://roqstar.s3.amazonaws.com/users/22682/items/1945-64vaxNrZ.jpg'

	return (
		<Card
			style={{ maxWidth: 280, margin: '10px 0 30px' }}
			title={
				<Meta
					title={props.game.name}
					style={{
						whiteSpace: 'nowrap',
						overflow: 'hidden',
						textOverflow: 'ellipsis'
					}}
				/>
			}
			cover={
				<Image alt='example' height={180} width={280} src={exampleImgUrl} />
			}
			bodyStyle={{
				whiteSpace: 'nowrap',
				overflow: 'hidden',
				textOverflow: 'ellipsis'
			}}
			footerLine={true}
			footerStyle={{ display: 'flex', justifyContent: 'flex-end' }}
			footer={
				<Space>
					<Button theme='solid' type='primary' onClick={props.onClick}>
						前往挑战
					</Button>
				</Space>
			}>
			{props.game.desc}
		</Card>
	)
}

export default GameCard
