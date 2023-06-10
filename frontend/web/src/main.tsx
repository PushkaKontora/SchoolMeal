import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './1_app/app/App.tsx'
import './1_app/styles/index.css'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
