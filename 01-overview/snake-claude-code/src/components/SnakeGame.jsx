import { useState, useEffect, useCallback, useRef } from 'react'

const GRID_SIZE = 20
const CELL_SIZE = 20

function SnakeGame() {
  const [snake, setSnake] = useState([{ x: 10, y: 10 }])
  const [food, setFood] = useState({ x: 15, y: 15 })
  const [direction, setDirection] = useState({ x: 0, y: 0 })
  const [gameOver, setGameOver] = useState(false)
  const [score, setScore] = useState(0)
  const [gameStarted, setGameStarted] = useState(false)
  const [mode, setMode] = useState('walls') // 'walls' or 'pass-through'

  const generateFood = useCallback(() => {
    let newFood
    do {
      newFood = {
        x: Math.floor(Math.random() * GRID_SIZE),
        y: Math.floor(Math.random() * GRID_SIZE)
      }
    } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y))
    return newFood
  }, [snake])

  const resetGame = () => {
    setSnake([{ x: 10, y: 10 }])
    setFood({ x: 15, y: 15 })
    setDirection({ x: 0, y: 0 })
    setGameOver(false)
    setScore(0)
    setGameStarted(false)
  }

  const moveSnake = useCallback(() => {
    if (!gameStarted || gameOver || (direction.x === 0 && direction.y === 0)) return

    setSnake(currentSnake => {
      const newSnake = [...currentSnake]
      const head = { ...newSnake[0] }
      
      head.x += direction.x
      head.y += direction.y

      if (mode === 'pass-through') {
        // Wrap around
        if (head.x < 0) head.x = GRID_SIZE - 1
        if (head.x >= GRID_SIZE) head.x = 0
        if (head.y < 0) head.y = GRID_SIZE - 1
        if (head.y >= GRID_SIZE) head.y = 0
      } else {
        // Walls mode: end game if out of bounds
        if (head.x < 0 || head.x >= GRID_SIZE || head.y < 0 || head.y >= GRID_SIZE) {
          setGameOver(true)
          return currentSnake
        }
      }

      if (newSnake.some(segment => segment.x === head.x && segment.y === head.y)) {
        setGameOver(true)
        return currentSnake
      }

      newSnake.unshift(head)

      if (head.x === food.x && head.y === food.y) {
        setScore(prev => prev + 5)
        setFood(generateFood())
      } else {
        newSnake.pop()
      }

      return newSnake
    })
  }, [direction, food, gameOver, gameStarted, generateFood, mode])

  const intervalRef = useRef(null)

  useEffect(() => {
    const handleKeyPress = (e) => {
      if (!gameStarted) {
        if (e.code === 'Space') {
          setGameStarted(true)
          setDirection({ x: 1, y: 0 })
        }
        return
      }

      if (gameOver) {
        if (e.code === 'Space') {
          resetGame()
        }
        return
      }

      switch (e.code) {
        case 'ArrowUp':
        case 'KeyW':
          if (direction.y === 0) setDirection({ x: 0, y: -1 })
          break
        case 'ArrowDown':
        case 'KeyS':
          if (direction.y === 0) setDirection({ x: 0, y: 1 })
          break
        case 'ArrowLeft':
        case 'KeyA':
          if (direction.x === 0) setDirection({ x: -1, y: 0 })
          break
        case 'ArrowRight':
        case 'KeyD':
          if (direction.x === 0) setDirection({ x: 1, y: 0 })
          break
      }
    }

    window.addEventListener('keydown', handleKeyPress)
    return () => window.removeEventListener('keydown', handleKeyPress)
  }, [direction, gameOver, gameStarted])

  useEffect(() => {
    if (intervalRef.current) clearInterval(intervalRef.current)
    intervalRef.current = setInterval(moveSnake, 150)
    return () => clearInterval(intervalRef.current)
  }, [moveSnake])

  return (
    <div className="flex flex-col items-center">
      <div className="mb-2">
        <button
          className="px-3 py-1 bg-gray-700 text-white rounded mb-2 disabled:opacity-50"
          onClick={() => setMode(mode === 'walls' ? 'pass-through' : 'walls')}
          disabled={gameStarted}
        >
          Switch to {mode === 'walls' ? 'Pass-Through' : 'Walls'} Mode
        </button>
        <div className="text-sm text-gray-300 mt-1">
          Mode: <span className="font-bold">{mode === 'walls' ? 'Walls' : 'Pass-Through'}</span>
        </div>
      </div>
      <div className="mb-4">
        <p className="text-xl">Score: {score}</p>
      </div>
      
      <div 
        className="relative bg-gray-800 border-2 border-gray-600"
        style={{
          width: GRID_SIZE * CELL_SIZE + 5,
          height: GRID_SIZE * CELL_SIZE + 5
        }}
      >
        {/* Grid lines */}
        {[...Array(GRID_SIZE + 1)].map((_, i) => (
          <div
            key={`v-${i}`}
            className="absolute bg-gray-700"
            style={{
              left: i === GRID_SIZE ? GRID_SIZE * CELL_SIZE - 1 : i * CELL_SIZE,
              top: 0,
              width: i === 0 || i === GRID_SIZE ? 2 : 1,
              height: GRID_SIZE * CELL_SIZE,
              opacity: 0.3,
              pointerEvents: 'none',
              zIndex: 1
            }}
          />
        ))}
        {[...Array(GRID_SIZE + 1)].map((_, i) => (
          <div
            key={`h-${i}`}
            className="absolute bg-gray-700"
            style={{
              top: i === GRID_SIZE ? GRID_SIZE * CELL_SIZE - 1 : i * CELL_SIZE,
              left: 0,
              height: i === 0 || i === GRID_SIZE ? 2 : 1,
              width: GRID_SIZE * CELL_SIZE,
              opacity: 0.3,
              pointerEvents: 'none',
              zIndex: 1
            }}
          />
        ))}
        {/* Snake */}
        {snake.map((segment, index) => (
          <div
            key={index}
            className={`absolute ${index === 0 ? 'bg-green-400' : 'bg-green-500'}`}
            style={{
              left: segment.x * CELL_SIZE + 1,
              top: segment.y * CELL_SIZE + 1,
              width: CELL_SIZE - 2,
              height: CELL_SIZE - 2,
              zIndex: 2
            }}
          />
        ))}
        {/* Food */}
        <div
          className="absolute bg-red-500"
          style={{
            left: food.x * CELL_SIZE + 1,
            top: food.y * CELL_SIZE + 1,
            width: CELL_SIZE - 2,
            height: CELL_SIZE - 2,
            zIndex: 2
          }}
        />
      </div>

      <div className="mt-4 text-center">
        {!gameStarted && !gameOver && (
          <p className="text-lg">Press SPACE to start</p>
        )}
        {gameOver && (
          <div>
            <p className="text-xl text-red-400 mb-2">Game Over!</p>
            <p className="text-lg">Press SPACE to restart</p>
          </div>
        )}
        {gameStarted && !gameOver && (
          <p className="text-sm text-gray-400">Use WASD or Arrow keys to move</p>
        )}
      </div>
    </div>
  )
}

export default SnakeGame