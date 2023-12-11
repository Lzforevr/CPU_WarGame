import TabBar from '../../components/TabBar.tsx'
import {
	useFieldState,
	Notification,
	Form,
	Button,
	InputGroup
} from '@douyinfe/semi-ui'
import { useState } from 'react'
import cookie from 'react-cookies'
import { serverUrl } from '../../data/constants.tsx'
import { Axios } from '../../tool/tool.tsx'

// 函数: 检查密码格式正确性
const checkPassword = (password: string) => {
	if (password.length < 8 || password.length > 14) {
		return '密码长度不符合要求！'
	} else if (password.match(/[\u4e00-\u9fa5]/)) {
		return '密码不能包含中文！'
	} else if (password.match(/\s/)) {
		return '密码不能包含空格！'
	} else {
		return '密码格式正确！'
	}
}

const PasswordInput = (props: { field: string }) => {
	// 提示文本
	let notifyText = '长度为8-14个字符, 不允许有空格、中文'
	// 密码状态
	const passwordState = useFieldState(props.field)
	// 密码格式验证
	if (passwordState.value !== undefined && passwordState.value !== '') {
		notifyText = checkPassword(passwordState.value)
	} else {
		notifyText = '长度为8-14个字符, 不允许有空格、中文'
	}

	return (
		<Form.Input
			noLabel={true}
			field={props.field}
			placeholder='密码'
			extraText={notifyText}
			style={{ width: '400px', height: '40px' }}
		/>
	)
}

const SendCaptchaButton = (props: { field: string }) => {
	// 设置状态：是否正在获取验证码, 再次获取验证码的时间
	const [isSending, setIsSending] = useState(false)
	const [waitTime, setWaitTime] = useState(0)
	const emailState = useFieldState(props.field)

	const sendCaptcha = async () => {
		// 验证邮箱格式
		if (emailState.value === undefined || emailState.value === '') {
			Notification.error({
				title: '邮箱不能为空！',
				duration: 2
			})
			return
		}
		if (
			!emailState.value.match(
				/^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+$/
			)
		) {
			// 检查邮箱格式是否符合:邮箱@域名
			Notification.error({
				title: '邮箱格式不正确！',
				duration: 2
			})
			return
		}
		// 发送请求
		Axios.post('/user/send_captcha', {
			email: emailState.value
		})
			.then(async response => {
				console.log(response)
				if (response.status === 200) {
					// 弹出提示框
					Notification.success({
						title: '验证码已发送至邮箱！',
						content: '请注意查收！',
						duration: 2
					})
					// 设置状态：正在获取验证码
					setIsSending(true)
					// 倒计时
					for (let i = 60; i > 0; i--) {
						setWaitTime(i)
						await new Promise(resolve => setTimeout(resolve, 1000))
					}
					setIsSending(false)
				} else if (response.status === 201) {
					Notification.error({
						title: '验证码发送失败！',
						content: '该邮箱已被注册！',
						duration: 2
					})
				}
			})
			.catch(err => {
				console.log(err)
			})
	}

	// 继承Button的属性
	return (
		<Button
			disabled={isSending}
			type='primary'
			theme='solid'
			style={{ width: '110px', marginLeft: '10px' }}
			onClick={sendCaptcha}>
			{isSending ? `${waitTime}s后重新获取` : '获取验证码'}
		</Button>
	)
}

const SignUp = () => {
	// 挂载时通过cookie检测是否已登录
	if (cookie.load('username') !== undefined) {
		window.location.href = '/'
	}

	const handleSubmit = (e: any) => {
		// 检查表单数据是否非空
		if (e.username === undefined || e.username === '') {
			Notification.error({
				title: '用户名不能为空！',
				duration: 2
			})
			return
		}
		if (e.email === undefined || e.email === '') {
			Notification.error({
				title: '邮箱不能为空！',
				duration: 2
			})
			return
		}
		if (e.password === undefined || e.password === '') {
			Notification.error({
				title: '密码不能为空！',
				duration: 2
			})
			return
		}
		if (e.captcha === undefined || e.captcha === '') {
			Notification.error({
				title: '验证码不能为空！',
				duration: 2
			})
			return
		}
		// 检查密码格式
		if (checkPassword(e.password) !== '密码格式正确！') {
			Notification.error({
				title: '密码格式不正确！',
				duration: 2
			})
			return
		}
		// 将数据转换为json格式
		const data = JSON.stringify(e)
		// 发送请求
		fetch(serverUrl + '/user/signUp?apifoxResponseId=278833023', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: data
		})
			.then(response => {
				console.log(response)
				if (response.status === 200) {
					window.location.href = '/login'
				} else if (response.status === 201) {
					Notification.error({
						title: '验证码错误！',
						content: '请重新输入！',
						duration: 2
					})
				}
			})
			.catch(err => {
				console.log(err)
			})
		// 阻止表单默认提交事件
		e.preventDefault()
	}

	return (
		// 注册表单
		<div style={{ width: '100%' }}>
			<TabBar />
			<Form
				className='login-form'
				onSubmit={e => {
					handleSubmit(e)
				}}>
				<h1>CPU Warframe</h1>
				<Form.Input
					noLabel={true}
					field='username'
					placeholder='用户名'
					style={{ width: '400px', height: '40px' }}
				/>
				<Form.Input
					noLabel={true}
					field='email'
					placeholder='邮箱'
					style={{ width: '400px', height: '40px' }}
				/>
				<PasswordInput field='password' />
				<InputGroup style={{ width: '400px', height: '40px' }}>
					<Form.Input
						noLabel={true}
						field='captcha'
						placeholder='验证码'
						style={{ width: '280px', height: '40px' }}
					/>
					<SendCaptchaButton field='email' />
				</InputGroup>
				<Button
					type='primary'
					theme='solid'
					htmlType='submit'
					style={{ width: '200px', margin: '20px auto' }}>
					注册
				</Button>
			</Form>
		</div>
	)
}

export default SignUp
