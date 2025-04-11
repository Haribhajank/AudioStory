import React, { useEffect, useState } from "react";
import jsPDF from "jspdf";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import { useNavigate } from "react-router-dom";

export default function EpisodeScripts() {
  const [episodes, setEpisodes] = useState<any[]>([]);
  const [scripts, setScripts] = useState<{ [key: number]: string[] }>({});
  const [generating, setGenerating] = useState<{ [key: number]: boolean }>({});
  const navigate = useNavigate();

  useEffect(() => {
    const numEpisodes = parseInt(localStorage.getItem("numEpisodes") || "0");
    setEpisodes(new Array(numEpisodes).fill(null));
  }, []);

  const generateScript = async (index: number) => {
    setGenerating((prev) => ({ ...prev, [index]: true }));
  
    try {
      const res = await fetch("http://localhost:8000/api/episodes/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ index }),  // ✅ send "index" key
      });
  
      const data = await res.json();
  
      if (res.ok && data.script_url) {
        const scriptRes = await fetch(`http://localhost:8000${data.script_url}`);
        const scriptJson = await scriptRes.json();
  
        if (Array.isArray(scriptJson)) {
          // if file contains raw array like ["line1", "line2"]
          setScripts((prev) => ({ ...prev, [index]: scriptJson }));
        } else if (Array.isArray(scriptJson.script)) {
          // if file contains { script: [...] }
          setScripts((prev) => ({ ...prev, [index]: scriptJson.script }));
        } else {
          alert("Script format invalid in script file.");
        }
      } else {
        alert("Script generation failed: " + (data.error || "Unknown error"));
      }
    } catch (err) {
      console.error("Script generation error:", err);
      alert("Something went wrong. Check backend logs.");
    }
  
    setGenerating((prev) => ({ ...prev, [index]: false }));
  };

  const downloadPDF = (script: string[], index: number) => {
    if (!script || script.length === 0) {
      alert("Script not available for this episode.");
      return;
    }

    const doc = new jsPDF();
    doc.setFont("Helvetica");
    doc.setFontSize(12);

    const pageHeight = doc.internal.pageSize.getHeight();
    const pageWidth = doc.internal.pageSize.getWidth();
    const marginLeft = 15;
    const marginTop = 20;
    const lineHeight = 8;
    const usableWidth = pageWidth - 2 * marginLeft;

    let currentY = marginTop;

    for (let line of script) {
      const wrappedLines = doc.splitTextToSize(line, usableWidth);
      for (let wrappedLine of wrappedLines) {
        if (currentY > pageHeight - 20) {
          doc.addPage();
          currentY = marginTop;
        }
        doc.text(wrappedLine, marginLeft, currentY);
        currentY += lineHeight;
      }
    }

    doc.save(`Episode_${index + 1}.pdf`);
  };

  const handleNext = () => navigate("/thumbnail");

  return (
    <div className="relative h-screen w-screen overflow-hidden">
      <img
        src="/home.png"
        alt="Background"
        className="absolute inset-0 w-full h-full object-cover"
      />
      <div className="fixed inset-0 bg-gradient-to-b from-black/40 via-black/20 to-transparent z-0 pointer-events-none" />

      <div className="relative z-10 h-full w-full overflow-y-auto px-4 py-12 flex justify-center items-start">
        <div className="w-full max-w-4xl">
          <h2 className="text-4xl font-bold text-center text-white mb-10 flex items-center justify-center gap-2">
            🎬 Generate Scripts for Episodes
          </h2>

          {episodes.length === 0 ? (
            <p className="text-center text-gray-300 text-lg">No episodes found.</p>
          ) : (
            <div className="space-y-6">
              {episodes.map((_, index) => (
                <Card
                  key={index}
                  className="bg-white/30 backdrop-blur-md shadow-xl border border-white/20 rounded-2xl"
                >
                  <CardContent className="p-6 space-y-4">
                    <h3 className="text-xl font-semibold text-gray-800">
                      📝 Episode {index + 1}
                    </h3>

                    {!scripts[index] ? (
                      <Button
                        onClick={() => generateScript(index)}
                        disabled={generating[index]}
                        className={`px-5 py-2 font-semibold rounded-md shadow-md transition-all ${
                          generating[index]
                            ? "bg-gray-300 text-gray-600 cursor-not-allowed animate-pulse"
                            : "bg-gradient-to-br from-pink-500 to-red-500 text-white hover:from-pink-600 hover:to-red-600"
                        }`}
                      >
                        {generating[index] ? "Generating..." : "Generate Script"}
                      </Button>
                    ) : (
                      <div className="space-y-4">
                        <p className="whitespace-pre-line leading-relaxed text-gray-800">
                        <div className="p-4 rounded-xl bg-white/60 shadow-md backdrop-blur-sm">{scripts[index].join("\n")}
                        </div>
                        </p>
                        <div className="text-center">
                          <Button
                            onClick={() => downloadPDF(scripts[index], index)}
                            className="px-5 py-2 rounded-md bg-black text-white font-semibold border border-white/20 
                              hover:bg-gray-900 hover:shadow-lg transition-all duration-300"
                          >
                            📄 Download PDF
                          </Button>
                        </div>
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {episodes.length > 0 && (
            <div className="text-center mt-12">
              <Button
                onClick={handleNext}
                className="px-8 py-4 rounded-xl bg-gradient-to-br from-fuchsia-600 to-pink-500 text-white font-bold text-lg shadow-xl 
                  hover:scale-105 hover:from-fuchsia-700 hover:to-pink-600 transition-all duration-300"
              >
                🚀 Next: Generate Thumbnails
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}