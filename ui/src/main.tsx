import '@shadcn/ui/global-css';
import './app.tailwind.css';
import './index.html';
import react from 'react';
import 'react-dom/client';
import App from './App';

const root = document.getElementById('root') as HTMLElement;
ReactDom.createRoot(root).render(
<React.strictMode><App/></React.strictMode>
);
