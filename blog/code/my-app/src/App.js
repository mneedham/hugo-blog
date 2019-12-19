import React, {Component, useEffect, useState} from 'react';
import './App.css';
import {globalHistory, Link, Router} from "@reach/router";


const Home = () => (
  <div>
    <h2>Home</h2>
  </div>
);

const Dashboard = () => (
  <div>
    <h2>Dashboard</h2>
  </div>
);

const Search = () => (
  <div>
    <h2>Search</h2>
  </div>
);


//
// class App extends Component {
//   constructor(props) {
//     super(props)
//     this.state = {
//       showSearchBox: true
//     };
//   }
//
//   componentDidMount() {
//     this.toggleSearchBox(globalHistory.location)
//
//     this.historyUnsubscribe = globalHistory.listen(({action, location}) => {
//       if (action === 'PUSH') {
//         this.toggleSearchBox(location)
//       }
//     });
//   }
//
//   componentWillUnmount() {
//     this.historyUnsubscribe();
//   }
//
//   toggleSearchBox(location) {
//     if (location.pathname === "/search") {
//       this.setState({
//         showSearchBox: false
//       })
//     } else {
//       this.setState({
//         showSearchBox: true
//       })
//     }
//   }
//
//   render() {
//     return (
//       <div className="App">
//         <header className="App-header">
//           <p>
//             React Reach Router Demo
//           </p>
//           <div>
//             {this.state.showSearchBox && <input type={"text"} style={{margin: "10px"}}/>}
//           </div>
//         </header>
//         <nav style={{padding: "5px"}}>
//           <Link to="/">Home</Link> <Link to="dashboard">Dashboard</Link> <Link to="search">Search</Link>
//         </nav>
//         <div style={{paddingTop: "10px"}}>
//           <Router>
//             <Home path="/"/>
//             <Dashboard path="/dashboard"/>
//             <Search path="/search"/>
//           </Router>
//         </div>
//       </div>
//     );
//   }
// }

function App() {
  const initialState = true

  const [showSearchBox, setShowSearchBox]= useState(initialState)
  useEffect(() => {
    const removeListener = globalHistory.listen(params => {
      const { location } = params;
      const newState = location.pathname !== "/search"
      setShowSearchBox(newState);
    });
    return () => {
      removeListener();
    };
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <p>React Reach Router Demo</p>
        <div>
          {showSearchBox && <input type={"text"} style={{ margin: "10px" }} />}
        </div>
      </header>
      <nav style={{ padding: "5px" }}>
        <Link to="/">Home</Link> <Link to="dashboard">Dashboard</Link>{" "}
        <Link to="search">Search</Link>
      </nav>
      <div style={{ paddingTop: "10px" }}>
        <Router>
          <Home path="/" />
          <Dashboard path="/dashboard" />
          <Search path="/search" />
        </Router>
      </div>
    </div>
  );
}

export default App;
