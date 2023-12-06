import { Card, Space, Button } from "@douyinfe/semi-ui";

const GameCard = (props) => {
    const { Meta } = Card;

    return (
        <Card
            style={{ maxWidth: 300, margin: '10px 0 30px' }}
            title={
                <Meta
                    title={props.name}
                />
            }
            cover={
                <img
                    alt="example"
                    src={props.imgUrl}
                />
            }
            bodyStyle={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}
            footerLine={ true }
            footerStyle={{ display: 'flex', justifyContent: 'flex-end' }}
            footer={
                <Space>
                    <Button disabled={true} theme='solid' type='primary'>前往挑战</Button>
                </Space>
            }
        >
            {props.desc}
        </Card>
    );
}

export default GameCard;