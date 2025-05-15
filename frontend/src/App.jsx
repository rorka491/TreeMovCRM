import React from 'react';
import Base from './components/base/base';

import { 
  Route,
  BrowserRouter as Router, 
  Routes 
} from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/*' element={<Base />} />
      </Routes>
    </Router>
  );
}

export default App;