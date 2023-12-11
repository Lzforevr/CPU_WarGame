import './LogIn.scss'
import TabBar from '../../components/TabBar.tsx'
import { Form, Button } from '@douyinfe/semi-ui'
import cookie from 'react-cookies'
import { serverUrl } from '../../data/constants.tsx'
import { Axios } from '../../tool/tool.tsx'

function LogIn() {
	// 挂载时通过cookie检测是否已登录
	if (cookie.load('username') !== undefined) {
		window.location.href = '/'
	}

	const handleSubmit = (e: any) => {
		console.log('log in')
		console.log(e)
		// 将数据转换为json格式
		const data = JSON.stringify(e)
		console.log(data)
		// 发送请求
		Axios.post('/user/login', data)
			.then((res) => {
				console.log(res)
				cookie.save('username', res.data.username, { path: '/' })
				cookie.save('email', res.data.email, { path: '/' })
				window.location.href = '/'
			})
			.catch(err => {
				console.log(err)
			})
		e.preventDefault()
	}

	const navToSignUp = () => {
		window.location.href = '/signUp'
	}

	return (
		// 登录表单
		<div style={{ width: '100%' }}>
			<TabBar />
			<Form
				className='login-form'
				onSubmit={(e: any) => {
					handleSubmit(e)
				}}>
				<h1>CPU Warframe</h1>
				<Form.Input
					noLabel={true}
					field='email'
					placeholder='邮箱'
					style={{ width: '400px', height: '40px' }}
				/>
				<Form.Input
					noLabel={true}
					field='password'
					placeholder='密码'
					style={{ width: '400px', height: '40px' }}
				/>
				<Button
					type='primary'
					htmlType='submit'
					theme='solid'
					style={{ width: '200px', margin: '10px auto 0' }}>
					登录
				</Button>
				<p>
					<span style={{ fontWeight: 'bold', marginRight: '5px' }}>Or</span>{' '}
					<Button type='primary' onClick={navToSignUp}>
						注册
					</Button>
				</p>
			</Form>
		</div>
	)
}

export default LogIn
