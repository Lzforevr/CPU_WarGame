import './Home.css';
import TabBar from '../../components/TabBar';

const Home = () => {
  window.location.href = '/games';
  
  return (
    <TabBar />
    // 一些炫酷且通用的首页元素

  );
}

export default Home;
