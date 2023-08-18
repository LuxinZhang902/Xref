import './App.css';
import 'antd/dist/reset.css'
import Footer from './components/Footer';
import MyRouter from "./router/index";
// import HeaderComponent from './components/HeaderComponent';

function App() {
  return (
    <div className = "page-container">
      {/* <HeaderComponent /> */}
      <div className="App">
        <MyRouter />
      </div>
      <Footer />
    </div>
  )
}

export default App;
