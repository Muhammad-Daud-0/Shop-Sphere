/* eslint-disable no-unused-vars */
export const API_BASE_URL = "http://mern-env.eba-qyah2eg7.ap-south-1.elasticbeanstalk.com/";

import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { BrowserRouter } from 'react-router-dom'
import { AuthProvider } from './context/auth.jsx'
import { SearchProvider } from './context/Search.jsx'
import "antd/dist/reset.css"
import { CartProvider } from './context/CartContext.jsx'
import { FavouriteProvider } from './context/FavouriteContext.jsx'

createRoot(document.getElementById('root')).render(
  <AuthProvider>
    <SearchProvider>
      <CartProvider>
        <FavouriteProvider>
          <BrowserRouter>
            <App />
          </BrowserRouter>
        </FavouriteProvider>
      </CartProvider>
    </SearchProvider>
  </AuthProvider>,
)
