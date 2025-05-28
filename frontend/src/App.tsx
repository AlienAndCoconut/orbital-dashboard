import {
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'
import './App.css'
import { UsageDashboard } from './components/UsageDashboard'
import { BrowserRouter } from 'react-router-dom';


const queryClient = new QueryClient()

function App() {
  return (
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        <UsageDashboard />
      </QueryClientProvider>
    </BrowserRouter>
  );
}

export default App
