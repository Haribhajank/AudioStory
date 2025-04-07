// // File: src/pages/StoryGenerator.tsx

// import React, { useState, useEffect } from "react";
// import { Button } from "../components/ui/button";
// import { Card, CardContent } from "../components/ui/card";
// import { useNavigate } from "react-router-dom";

// export default function StoryGenerator() {
//   const [masterDoc, setMasterDoc] = useState<{ title: string; plot: string } | null>(null);
//   const [loading, setLoading] = useState(false);
//   const navigate = useNavigate();

//   // ✅ Get idea from localStorage
//   const idea = localStorage.getItem("idea");

//   const generateMasterDoc = async () => {
//     if (!idea) return;

//     setLoading(true);
//     const res = await fetch("http://localhost:8000/api/story/", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ idea }),
//     });

//     const data = await res.json();
//     setMasterDoc(data);
//     setLoading(false);
//   };

//   const handleApprove = () => {
//     if (!masterDoc) return;
//     localStorage.setItem("masterDoc", JSON.stringify(masterDoc));
//     navigate("/scripts");
//   };

//   // 🔁 Auto-generate on first render
//   useEffect(() => {
//     generateMasterDoc();
//   }, []);

//   return (
//     <div className="min-h-screen bg-white flex flex-col items-center justify-center p-4">
//       <h1 className="text-3xl font-bold mb-6 text-center max-w-xl">
//         Generated Plot for Your Story
//       </h1>

//       {loading && <p className="text-gray-500">Generating story plot...</p>}

//       {masterDoc && (
//         <Card className="mt-4 w-full max-w-2xl">
//           <CardContent className="space-y-4">
//             <h2 className="text-xl font-semibold">{masterDoc.title}</h2>
//             <p>{masterDoc.plot}</p>
//             <div className="flex gap-4 mt-4">
//               <Button variant="outline" onClick={generateMasterDoc}>Regenerate</Button>
//               <Button onClick={handleApprove}>Approve & Proceed</Button>
//             </div>
//           </CardContent>
//         </Card>
//       )}
//     </div>
//   );
// }

// import React, { useState, useEffect } from "react";
// import { Button } from "../components/ui/button";
// import { Card, CardContent } from "../components/ui/card";
// import { useNavigate } from "react-router-dom";

// export default function StoryGenerator() {
//   const [masterDoc, setMasterDoc] = useState<{ title: string; plot: string } | null>(null);
//   const [loading, setLoading] = useState(false);
//   const navigate = useNavigate();

//   const idea = localStorage.getItem("idea");

//   const generateMasterDoc = async () => {
//     if (!idea) return;

//     setLoading(true);
//     const res = await fetch("http://localhost:8000/api/story/", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ idea }),
//     });

//     const data = await res.json();
//     setMasterDoc(data);
//     setLoading(false);
//   };

//   const handleApprove = () => {
//     if (!masterDoc) return;
//     localStorage.setItem("masterDoc", JSON.stringify(masterDoc));
//     navigate("/scripts");
//   };

//   useEffect(() => {
//     generateMasterDoc();
//   }, []);

//   return (
//     <div
//       className="min-h-screen flex flex-col items-center justify-center p-4 bg-cover bg-center"
//       style={{ backgroundImage: "url('/home.png')" }}
//     >
//       <h1 className="text-4xl font-bold text-center text-white drop-shadow-md mb-6">
//         Generated Plot for Your Story
//       </h1>

//       {loading && <p className="text-gray-100 text-lg">Generating story plot...</p>}

//       {masterDoc && (
//         <Card className="mt-4 w-full max-w-2xl bg-white/90 backdrop-blur-md">
//           <CardContent className="space-y-4">
//             <h2 className="text-xl font-semibold">{masterDoc.title}</h2>
//             <p>{masterDoc.plot}</p>
//             <div className="flex gap-4 mt-4 justify-center">
//               {/* <Button variant="outline" onClick={generateMasterDoc}>Regenerate</Button> */}
//               <Button  onClick={generateMasterDoc}>Regenerate</Button>
//               <Button onClick={handleApprove}>Approve & Proceed</Button>
//             </div>
//           </CardContent>
//         </Card>
//       )}
//     </div>
//   );
// }
import React, { useState, useEffect } from "react";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import { useNavigate } from "react-router-dom";

export default function StoryGenerator() {
  const [masterDoc, setMasterDoc] = useState<{ title: string; plot: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const idea = localStorage.getItem("idea");

  const generateMasterDoc = async () => {
    if (!idea) return;

    setLoading(true);
    const res = await fetch("http://localhost:8000/api/story/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ idea }),
    });

    const data = await res.json();
    setMasterDoc(data);
    setLoading(false);
  };

  const handleApprove = () => {
    if (!masterDoc) return;
    localStorage.setItem("masterDoc", JSON.stringify(masterDoc));
    navigate("/scripts");
  };

  useEffect(() => {
    generateMasterDoc();
  }, []);

  return (
    <div className="relative w-screen h-screen overflow-hidden">
      {/* 🌄 Fullscreen Background */}
      <div
        className="fixed inset-0 bg-cover bg-center z-0"
        style={{ backgroundImage: "url('/home.png')" }}
      />
      <div className="fixed inset-0 bg-gradient-to-b from-black/40 via-black/20 to-transparent z-0 pointer-events-none" />

      {/* 💡 Foreground Content */}
      <div className="relative z-10 flex flex-col items-center justify-center w-full h-full px-4 text-white text-center">
        <h1 className="text-4xl sm:text-5xl font-black drop-shadow-md mb-8">
          Generated Plot for Your Story
        </h1>

        {/* 🌀 Loading Spinner */}
        {loading && (
          <div className="flex flex-col items-center gap-4 animate-pulse">
            <svg
              className="w-10 h-10 animate-spin text-white"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v8z"
              />
            </svg>
            <p className="text-lg">Generating your story magic...</p>
          </div>
        )}

        {/* 📖 Plot Card */}
        {masterDoc && (
        <div className="w-full max-w-3xl px-4 animate-fade-in-up transition-all duration-500 ease-out">
          <Card className="bg-white/30 backdrop-blur-md shadow-xl border border-white/20 rounded-2xl">
            <CardContent className="space-y-4 p-6 text-black">
              <h2 className="text-xl font-semibold">{masterDoc.title}</h2>
              <p className="text-gray-800">{masterDoc.plot}</p>
              <div className="flex gap-4 mt-4 justify-center">
              <Button
                className="px-6 py-3 rounded-lg bg-white/10 text-white font-semibold shadow-md border border-white/30 backdrop-blur-md 
                          hover:bg-white/20 hover:shadow-lg transition-all duration-300"
                onClick={generateMasterDoc}
              >
                Regenerate
              </Button>

              <Button
                className="px-6 py-3 rounded-lg bg-black text-white font-semibold shadow-md border border-white/20 
                          hover:bg-gray-900 hover:shadow-lg transition-all duration-300"
                onClick={handleApprove}
              >
                Approve & Proceed
              </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
  
          {/* 📝 Note */}
          {!masterDoc && !loading && (
            <p className="text-gray-300 mt-4">Your plot will appear here...</p>
          )}
      </div>
    </div>
  );
}


