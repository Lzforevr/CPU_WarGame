import { Space } from '@douyinfe/semi-ui'
import { Align } from '@douyinfe/semi-ui/lib/es/space'

export const Window = (props: { children: React.ReactNode | undefined, align?: Align }) => {
    //获取浏览器高度
    const height = window.innerHeight

	return (
		<Space vertical={true} align='center' style={{ width: '100%' }}>
			<Space
				vertical={true}
				align={props.align ?? 'center'}
				style={{
					width: '80%',
                    height: 'fit-content',
                    minHeight: height * 0.8,
					backgroundColor: 'rgba(var(--semi-grey-0), 0.8)',
					borderRadius: '10px',
					margin: '20px 0',
					padding: '20px'
				}}>
				{props.children}
			</Space>
		</Space>
	)
}
