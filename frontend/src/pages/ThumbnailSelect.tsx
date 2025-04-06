// File: src/pages/ThumbnailSelect.tsx

import React, { useEffect, useState } from "react";
import { Button } from "../components/ui/button";
import { useNavigate } from "react-router-dom";

export default function ThumbnailSelect() {
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
    const res = await fetch("http://localhost:8000/api/thumbnails/", {
      method: "POST",
      body: JSON.stringify({ title: masterDoc.title, plot: masterDoc.plot }),
      headers: { "Content-Type": "application/json" },
    });
    const data = await res.json();
    setThumbnails(data.thumbnails); // array of image URLs or base64
    setLoading(false);
  };

  const generateFinalImage = async () => {
    if (selected === null) return;
    const res = await fetch("http://localhost:8000/api/final-image/", {
      method: "POST",
      body: JSON.stringify({ prompt: thumbnails[selected] }),
      headers: { "Content-Type": "application/json" },
    });
    const data = await res.json();
    setFinalImageUrl(data.image);
  };

  return (
    <div className="min-h-screen p-4 bg-white">
      <h2 className="text-2xl font-bold mb-4 text-center">Select a Thumbnail</h2>
      {loading ? (
        <p className="text-center">Generating thumbnails...</p>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {thumbnails.map((src, idx) => (
            <img
              key={idx}
              src={src}
              alt={`Thumbnail ${idx + 1}`}
              className={`rounded-lg cursor-pointer border-4 transition-all duration-300 ${
                selected === idx ? "border-blue-500" : "border-transparent"
              }`}
              onClick={() => setSelected(idx)}
            />
          ))}
        </div>
      )}

      {selected !== null && !finalImageUrl && (
        <div className="text-center mt-6">
          <Button onClick={generateFinalImage}>Generate Final Image</Button>
        </div>
      )}

      {finalImageUrl && (
        <div className="mt-6 text-center">
          <h3 className="text-lg font-semibold mb-2">Final Thumbnail</h3>
          <img
            src={finalImageUrl}
            alt="Final Thumbnail"
            className="mx-auto rounded-xl border shadow-md max-w-sm"
          />
          <a
            href={finalImageUrl}
            download="final_thumbnail.png"
            className="block mt-4 text-blue-600 hover:underline"
          >
            Download Final Thumbnail
          </a>
          <div className="mt-4">
            <Button onClick={() => navigate("/audio")}>Next: Generate Audio</Button>
          </div>
        </div>
      )}
    </div>
  );
}
