// File: src/pages/AudioGenerator.tsx

import React, { useEffect, useState } from "react";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";

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
    const res = await fetch("http://localhost:8000/api/audio/", {
      method: "POST",
      body: JSON.stringify({ script: episodes[index].script }),
      headers: { "Content-Type": "application/json" },
    });
    const data = await res.json();
    setAudioLinks((prev) => ({ ...prev, [index]: data.audio_url }));
    setGenerating((prev) => ({ ...prev, [index]: false }));
  };

  return (
    <div className="min-h-screen bg-white p-4 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-4 text-center">Generate Audio for Episodes</h2>

      {episodes.length === 0 ? (
        <p className="text-center">No episodes found.</p>
      ) : (
        <div className="space-y-4">
          {episodes.map((ep, index) => (
            <Card key={index}>
              <CardContent className="p-4 space-y-2">
                <h3 className="font-semibold">Episode {index + 1}</h3>

                {!audioLinks[index] ? (
                  <Button
                    onClick={() => generateAudio(index)}
                    disabled={generating[index]}
                  >
                    {generating[index] ? "Generating..." : "Generate Audio"}
                  </Button>
                ) : (
                  <div className="space-y-2">
                    <audio controls src={audioLinks[index]} className="w-full" />
                    <a
                      href={audioLinks[index]}
                      download={`Episode_${index + 1}.mp3`}
                      className="text-blue-600 hover:underline"
                    >
                      Download Audio
                    </a>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
