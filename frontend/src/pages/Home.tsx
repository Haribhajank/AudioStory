// // src/pages/Home.tsx
// import { useNavigate } from 'react-router-dom'
// import { useState } from 'react'
// import { Input } from "../components/ui/input"
// import { Button } from "../components/ui/button"

// export default function Home() {
//   const [idea, setIdea] = useState("")
//   const navigate = useNavigate()

//   const handleSubmit = () => {
//     if (!idea.trim()) return

//     // ✅ Save the idea to localStorage
//     localStorage.setItem("idea", idea)

//     // ✅ Let /story page generate the master doc
//     navigate("/story")
//   }

//   return (
//     <div className="min-h-screen flex flex-col items-center justify-center px-4">
//       <h1 className="text-3xl font-bold mb-4 text-center">
//         Turn your idea into a fully narrated visual story
//       </h1>
//       <Input
//         value={idea}
//         onChange={(e) => setIdea(e.target.value)}
//         placeholder="Enter your idea, trope, or plot..."
//         className="max-w-md mb-4"
//       />
//       <Button onClick={handleSubmit}>Submit</Button>
//     </div>
//   )
// }

import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function Home() {
  const [idea, setIdea] = useState("");
  const navigate = useNavigate();

  const handleSubmit = () => {
    if (!idea.trim()) return;
    localStorage.setItem("idea", idea);
    navigate("/story");
  };

  return (
    <div className="relative h-screen w-screen overflow-hidden">
      {/* Background Image */}
      <img
        src="/home.png"
        alt="Narrated visual story background"
        className="absolute inset-0 w-full h-full object-cover"
      />

      {/* Overlay */}
      {/* <div className="absolute inset-0 bg-black bg-opacity-30" /> */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/40 via-black/20 to-transparent z-0 pointer-events-none" />


      {/* Foreground */}
      <div className="relative z-10 flex flex-col items-center justify-center h-full px-4 text-white text-center">
        <div className="flex flex-col gap-8 items-center -mt-36 sm:-mt-44 md:-mt-52 w-full px-4">
          {/* Heading */}
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-black leading-tight drop-shadow-lg">
            Turn your idea into a
            <br />
            fully narrated visual story
          </h1>

          {/* Input + Button */}
          <div className="flex flex-col sm:flex-row items-center gap-4 w-full max-w-xl">
          <textarea
              value={idea}
              onChange={(e) => setIdea(e.target.value)}
              placeholder="Enter your idea, trope, or plot..."
              rows={2}
              className="w-full px-6 py-4 text-black placeholder-gray-700 bg-white/60 rounded-xl shadow-inner backdrop-blur-lg border border-white/40 focus:outline-none focus:ring-2 focus:ring-white transition duration-200 text-lg resize-y min-h-[3rem] max-h-[12rem] overflow-auto"
            />
            <button
              onClick={handleSubmit}
              className="px-6 py-4 bg-gradient-to-br from-black to-gray-800 text-white font-semibold rounded-xl hover:from-gray-900 hover:to-black transition duration-200 shadow-lg"
            >
              Submit
            </button>
          </div>

        </div>
      </div>
    </div>
  );
}


