import { useState, useEffect } from 'react';
import TabBar from '../../components/TabBar';
import { Col, Divider, Row, Typography } from '@douyinfe/semi-ui';
import GameCard from '../../components/GameCard';
import serverConfig from '../../serverConfig.json';

const serverUrl = serverConfig.serverUrl;

const Games = () => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [gameTypes, setGameTypes] = useState([]);
  const [games, setGames] = useState({});
  const { Title } = Typography;

  useEffect(() => {
    fetch(serverUrl + '/getProjects', {
      method: 'GET',
    })
      .then((res) => res.json())
      .then((data) => {
        const newGameTypes = [];
        const newGames = {};

        for (let key of Object.keys(data)) {
          newGameTypes.push(key);
          data[key] = data[key].map((item) => (
            <Col key={item.id} span={6}>
              <GameCard id={item.id} name={item.name} desc={item.desc} imgUrl={item.imgUrl} />
            </Col>
          ));
          newGames[key] = data[key];
        }

        setGameTypes(newGameTypes);
        setGames(newGames);
        setIsLoaded(true);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []); // Empty dependency array ensures this effect runs only once on component mount.

  return (
    <div className="games">
      <TabBar />
      {isLoaded ? (
        <div className="games-grid" style={{margin: '20px 50px'}}>
          {
            gameTypes.map((item) => (
              <div key={item}>
                <Title level={2}>{`${item} >>`}</Title>
                <Divider margin={10}/>
                <Row gutter={2}>
                  {games[item]}
                </Row>
              </div>
            ))
          }
        </div>
      ) : null}
    </div>
  );
}

export default Games;
