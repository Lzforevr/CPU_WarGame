import { Nav, Avatar } from '@douyinfe/semi-ui'
import { IconAlarm, IconHistogram, IconServer } from '@douyinfe/semi-icons'
import { useState, useEffect } from 'react'
import cookie from 'react-cookies'

function TabBar() {
    // 定义状态：是否登录
    const [isLogin, setIsLogin] = useState(false)
    const [userInfo, setUserInfo] = useState({username: '', email: ''})

    // 挂载到DOM之前执行
    useEffect(() => {
        // 获取cookie
        const username = cookie.load('username')
        const email = cookie.load('email')
        // 如果cookie存在
        if (username && email && username !== '' && email !== '' && isLogin === false) {
            // 修改登录状态
            setUserInfo({username: username, email: email})
            console.log(userInfo)
            setIsLogin(true)
        }
    }, [userInfo, isLogin])

    const navToLogIn = () => {
        window.location.href = '/login'
    }

    const logOut = () => {
        if(window.confirm("确定要退出登录吗？") === true) {
            cookie.remove('username', {path: '/'})
            cookie.remove('email', {path: '/'})
            setIsLogin(false)
            window.location.href = '/'
        }
    }

    return (
        <div style={{ width: '100%' }}>
            <Nav
                type="primary"
                mode="horizontal"
                defaultSelectedKeys={['1']}
            >
                <Nav.Header text="CPU Warframe" link='/'/>
                <Nav.Item key="1" text="闯关项目" icon={<IconAlarm />} link='/games'/>
                <Nav.Item key="2" text="积分排行" icon={<IconHistogram/>} link='/rank'/>
                <Nav.Item key="3" text="知识库" icon={<IconServer /> } link='/library'/>
                <Nav.Footer children={
                    <div className='user-info' onClick={isLogin ? logOut : navToLogIn}>
                        <Avatar size="small" color='light-blue' style={{ margin: 4 }}>U</Avatar>
                        <span>{isLogin ? userInfo.username : "请登录" }</span>
                    </div>
                }/>
            </Nav>
        </div>
    );
}

export default TabBar;