// File: src/pages/EpisodeScripts.tsx

import React, { useEffect, useState } from "react";
import jsPDF from "jspdf";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from "../components/ui/accordion";
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

  return (
    <div className="min-h-screen bg-white p-4 max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-4 text-center">Episode Scripts</h2>
      {loading ? (
        <p className="text-center">Generating episodes...</p>
      ) : (
        <Accordion type="multiple" className="space-y-2">
          {episodes.map((ep: any, index: number) => (
            <AccordionItem value={`ep-${index}`} key={index}>
              <AccordionTrigger>Episode {index + 1}</AccordionTrigger>
              <AccordionContent>
                <Card>
                  <CardContent className="py-4 space-y-2">
                    <p className="whitespace-pre-line">{ep.script}</p>
                    <Button
                        onClick={() => {
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
                        }}
                        >
                        Download PDF
                        </Button>
                  </CardContent>
                </Card>
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      )}

      {!loading && episodes.length > 0 && (
        <div className="text-center mt-6">
          <Button onClick={handleNext}>Next: Generate Thumbnails</Button>
        </div>
      )}
    </div>
  );
}
