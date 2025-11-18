import SnakeGame from './components/SnakeGame'

function App() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
      <h1 className="text-4xl font-bold mb-4">Snake Game</h1>
      <SnakeGame />
    </div>
  )
}

export default App
