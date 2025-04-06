// src/pages/Home.tsx
import { useNavigate } from 'react-router-dom'
import { useState } from 'react'
import { Input } from "../components/ui/input"
import { Button } from "../components/ui/button"

export default function Home() {
  const [idea, setIdea] = useState("")
  const navigate = useNavigate()

  const handleSubmit = () => {
    if (!idea.trim()) return

    // ✅ Save the idea to localStorage
    localStorage.setItem("idea", idea)

    // ✅ Let /story page generate the master doc
    navigate("/story")
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4">
      <h1 className="text-3xl font-bold mb-4 text-center">
        Turn your idea into a fully narrated visual story
      </h1>
      <Input
        value={idea}
        onChange={(e) => setIdea(e.target.value)}
        placeholder="Enter your idea, trope, or plot..."
        className="max-w-md mb-4"
      />
      <Button onClick={handleSubmit}>Submit</Button>
    </div>
  )
}

