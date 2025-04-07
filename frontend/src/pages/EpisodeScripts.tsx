import React, { useEffect, useState } from "react";
import jsPDF from "jspdf";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import {
  Accordion,
  AccordionItem,
  AccordionTrigger,
  AccordionContent,
} from "../components/ui/accordion";
import { useNavigate } from "react-router-dom";

export default function EpisodeScripts() {
  const [episodes, setEpisodes] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      const masterDoc = JSON.parse(localStorage.getItem("masterDoc") || "null");
      if (!masterDoc) {
        navigate("/");
        return;
      }
      await generateEpisodes(masterDoc);
    };
    fetchData();
  }, []);

  const generateEpisodes = async (masterDoc: any) => {
    setLoading(true);
    const res = await fetch("http://localhost:8000/api/episodes/", {
      method: "POST",
      body: JSON.stringify({ title: masterDoc.title, plot: masterDoc.plot }),
      headers: { "Content-Type": "application/json" },
    });
    const data = await res.json();
    setEpisodes(data.episodes);
    localStorage.setItem("episodes", JSON.stringify(data.episodes));
    setLoading(false);
  };

  const handleNext = () => navigate("/thumbnail");

  const downloadPDF = (ep: any, index: number) => {
    const scriptArray = Array.isArray(ep) ? ep : ep.script;

    if (!Array.isArray(scriptArray) || scriptArray.length === 0) {
      alert("Script not available or invalid for this episode.");
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

    for (let line of scriptArray) {
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

  return (
    <div className="relative min-h-screen w-full mx-80 overflow-hidden">
      {/* 🌄 Background */}
      <div
        className="fixed inset-0 bg-cover bg-center z-0"
        style={{ backgroundImage: "url('/home.png')" }}
      />
      <div className="fixed inset-0 bg-gradient-to-b from-black/40 via-black/20 to-transparent z-0 pointer-events-none" />

      {/* 🎬 Foreground */}
      <div className="relative z-10  flex mr-12 flex-col items-center justify-center text-white min-h-screen w-full px-4 py-12">
        <div className="w-full max-w-4xl text-center">
          <h2 className="text-4xl sm:text-5xl font-bold mb-10 drop-shadow-lg flex items-center justify-center gap-3">
            <span role="img" aria-label="clapperboard">🎬</span> Episode Scripts
          </h2>

          {loading ? (
            <div className="text-center animate-pulse">
              <svg className="w-8 h-8 mx-auto animate-spin" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="white" strokeWidth="4" />
                <path className="opacity-75" fill="white" d="M4 12a8 8 0 018-8v8z" />
              </svg>
              <p className="mt-2">Generating episodes...</p>
            </div>
          ) : (
            <div className="flex justify-center w-full">
            <Accordion type="multiple" className="w-full max-w-2xl flex flex-col gap-6">
              {episodes.map((ep: any, index: number) => (
                <AccordionItem
                  value={`ep-${index}`}
                  key={index}
                  className="w-full max-w-xl bg-white/10 rounded-xl backdrop-blur-md shadow-md border border-white/20"
                >
                  <AccordionTrigger className="px-6 py-4 text-lg font-semibold text-white hover:bg-white/10 transition-colors">
                    📘 Episode {index + 1}
                  </AccordionTrigger>
                  <AccordionContent className="bg-white/30 backdrop-blur-md rounded-b-xl text-black px-6 py-4">
                    <Card className="bg-white/60 border border-white/30 rounded-xl shadow-md">
                      <CardContent className="p-6 space-y-4">
                        <p className="whitespace-pre-line leading-relaxed">{ep.script}</p>
                        <div className="flex justify-center">
                          <Button
                            onClick={() => downloadPDF(ep, index)}
                            className="px-5 py-2 rounded-md bg-black text-white font-semibold border border-white/20 
                              hover:bg-gray-900 hover:shadow-lg transition-all duration-300"
                          >
                            📄 Download PDF
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
            </div>
          )}

          {!loading && episodes.length > 0 && (
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
