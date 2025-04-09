// File: src/pages/ThumbnailSelect.tsx

import React, { useEffect, useState } from "react";
import { Button } from "../components/ui/button";
import { useNavigate } from "react-router-dom";
import { ImageIcon } from "lucide-react";

export default function ThumbnailSelect() {
  const BASE_BACKEND_URL = "http://127.0.0.1:8000";
  const [thumbnails, setThumbnails] = useState<string[]>([]);
  const [selected, setSelected] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [finalImageUrl, setFinalImageUrl] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchThumbnails = async () => {
      const masterDoc = JSON.parse(localStorage.getItem("masterDoc") || "null");
      if (!masterDoc) {
        navigate("/");
        return;
      }
      await generateThumbnails(masterDoc);
    };

    fetchThumbnails();
  }, []);

  const generateThumbnails = async (masterDoc: any) => {
    setLoading(true);
    const res = await fetch(`${BASE_BACKEND_URL}/api/thumbnails/`, {
      method: "POST",
      body: JSON.stringify({ title: masterDoc.title, plot: masterDoc.plot }),
      headers: { "Content-Type": "application/json" },
    });
    const data = await res.json();
    setThumbnails(data.thumbnails);
    setLoading(false);
  };

  const generateFinalImage = async () => {
    if (selected === null) return;

    const res = await fetch(`${BASE_BACKEND_URL}/api/final-image/`, {
      method: "POST",
      body: JSON.stringify({ prompt_index: selected }),
      headers: { "Content-Type": "application/json" },
    });

    const data = await res.json();
    setFinalImageUrl(`${BASE_BACKEND_URL}${data.image}`);
    setThumbnails([]);
  };

  return (
    <div className="relative min-h-screen w-screen overflow-y-auto bg-black">
      {/* Background Image */}
      <img
        src="/thumbnail.png"
        alt="Narrated visual story background"
        className="absolute inset-0 w-full h-full object-cover"
      />

      {/* Overlay */}
      {/* <div className="absolute inset-0 bg-black bg-opacity-30" /> */}
      {/* <div className="absolute inset-0 bg-gradient-to-b from-black/40 via-black/20 to-transparent z-0 pointer-events-none" /> */}
  
    {/* Foreground content */}
    <div className="relative z-10 flex flex-col items-center justify-start py-12 px-4 min-h-screen">
    <div className="min-h-screen w-full  flex flex-col items-center justify-start py-12 px-4">
        {/* Heading */}
        <h2 className="text-4xl font-bold text-gray-800 mb-10 flex items-center gap-3">
          <ImageIcon className="w-8 h-8 text-blue-500" /> Choose Your Favorite Thumbnail
        </h2>
  
        {/* Thumbnails */}
        {loading ? (
          <p className="text-center text-lg text-gray-600">✨ Generating thumbnails...</p>
        ) : !finalImageUrl && thumbnails.length > 0 ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-6 justify-center">
            {thumbnails.map((src, idx) => (
              <img
                key={idx}
                src={`${BASE_BACKEND_URL}${src}`}
                alt={`Thumbnail ${idx + 1}`}
                onClick={() => setSelected(idx)}
                className={`rounded-xl cursor-pointer border-4 transition-all duration-300 shadow-md hover:scale-105 ${
                  selected === idx ? "border-blue-500 shadow-lg" : "border-transparent"
                }`}
              />
            ))}
          </div>
        ) : null}
  
        {/* Generate Final Image Button */}
        {selected !== null && !finalImageUrl && (
          <div className="text-center mt-8">
            <Button
              onClick={generateFinalImage}
              className="px-6 py-3 rounded-lg bg-gradient-to-br from-indigo-600 to-purple-500 text-white font-bold shadow-lg hover:scale-105 transition"
            >
              🚀 Generate Final Image
            </Button>
          </div>
        )}
  
        {/* Final Thumbnail View */}
        {finalImageUrl && (
          <div className="mt-12 text-center">
            <h3 className="text-2xl font-semibold mb-4">🎉 Final Thumbnail</h3>
            <img
              src={`${finalImageUrl}?${Date.now()}`}
              alt="Final Thumbnail"
              className="mx-auto rounded-xl border shadow-xl max-w-sm"
            />
            <div className="mt-6 space-y-4">
              <a
                href={`${finalImageUrl}?${Date.now()}`}
                download="final_thumbnail.png"
                className="inline-block text-blue-600 hover:underline font-medium"
              >
                ⬇️ Download Final Thumbnail
              </a>
              <div>
                <Button
                  onClick={() => navigate("/audio")}
                  className="px-6 py-3 rounded-lg bg-gradient-to-br from-pink-600 to-red-500 text-white font-bold shadow-lg hover:scale-105 transition"
                >
                  🎧 Next: Generate Audio
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  </div>
  );
}


