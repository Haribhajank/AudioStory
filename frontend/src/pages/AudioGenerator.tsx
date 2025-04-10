import React, { useEffect, useState } from "react";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import { MusicIcon } from "lucide-react";

export default function AudioGenerator() {
  const [episodes, setEpisodes] = useState<any[]>([]);
  const [audioLinks, setAudioLinks] = useState<{ [key: number]: string }>({});
  const [generating, setGenerating] = useState<{ [key: number]: boolean }>({});

  useEffect(() => {
    const savedEpisodes = JSON.parse(localStorage.getItem("episodes") || "[]");
    setEpisodes(savedEpisodes);
  }, []);

  const generateAudio = async (index: number) => {
    setGenerating((prev) => ({ ...prev, [index]: true }));

    try {
      const res = await fetch("http://localhost:8000/api/audio/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ episode_index: index }),
      });

      const data = await res.json();

      if (res.ok) {
        setAudioLinks((prev) => ({ ...prev, [index]: data.audio_url }));
      } else {
        alert("Audio generation failed: " + (data.error || "Unknown error"));
      }
    } catch (err) {
      console.error("Audio generation error:", err);
      alert("Something went wrong. Check backend logs.");
    }

    setGenerating((prev) => ({ ...prev, [index]: false }));
  };

  return (
    <div className="relative h-screen w-screen overflow-hidden">
  {/* Background Image */}
  <img
    src="/audio.png"
    alt="Narrated visual story background"
    className="absolute inset-0 w-full h-full object-cover"
  />

  {/* Scrollable Foreground Content */}
  <div className="relative z-10 h-full w-full overflow-y-auto px-4 py-12 flex justify-center items-start">
    <div className="w-full max-w-4xl">
      <h2 className="text-4xl font-bold text-center text-gray-800 mb-10 flex items-center justify-center gap-2">
        <MusicIcon className="w-7 h-7 text-indigo-600" /> Generate Audio for Episodes
      </h2>

      {episodes.length === 0 ? (
        <p className="text-center text-gray-600 text-lg">No episodes found.</p>
      ) : (
        <div className="space-y-6">
          {episodes.map((_, index) => (
            <Card
              key={index}
              className="bg-white/80 backdrop-blur-sm opacity-90 border border-white/40 shadow-md rounded-xl"
            >
              <CardContent className="p-6 space-y-4">
                <h3 className="text-xl font-semibold text-gray-800">
                  🎙️ Episode {index + 1}
                </h3>

                {!audioLinks[index] ? (
                  <Button
                    onClick={() => generateAudio(index)}
                    disabled={generating[index]}
                    className={`px-5 py-2 font-semibold rounded-md shadow-md transition-all ${
                      generating[index]
                        ? "bg-gray-300 text-gray-600 cursor-not-allowed animate-pulse"
                        : "bg-gradient-to-br from-indigo-500 to-purple-500 text-white hover:from-indigo-600 hover:to-purple-600"
                    }`}
                  >
                    {generating[index] ? "Generating..." : "Generate Audio"}
                  </Button>
                ) : (
                  <div className="space-y-3">
                    <audio
                      controls
                      src={`http://localhost:8000${audioLinks[index]}`}
                      className="w-full rounded-lg"
                    />
                    <a
                      href={`http://localhost:8000${audioLinks[index]}`}
                      download={`Episode_${index + 1}.wav`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-block text-blue-600 hover:underline"
                    >
                      ⬇️ Download Audio
                    </a>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  </div>
</div>
  );
}
