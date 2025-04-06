// File: src/pages/StoryGenerator.tsx

import React, { useState, useEffect } from "react";
import { Button } from "../components/ui/button";
import { Card, CardContent } from "../components/ui/card";
import { useNavigate } from "react-router-dom";

export default function StoryGenerator() {
  const [masterDoc, setMasterDoc] = useState<{ title: string; plot: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // ✅ Get idea from localStorage
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

  // 🔁 Auto-generate on first render
  useEffect(() => {
    generateMasterDoc();
  }, []);

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-4">
      <h1 className="text-3xl font-bold mb-6 text-center max-w-xl">
        Generated Plot for Your Story
      </h1>

      {loading && <p className="text-gray-500">Generating story plot...</p>}

      {masterDoc && (
        <Card className="mt-4 w-full max-w-2xl">
          <CardContent className="space-y-4">
            <h2 className="text-xl font-semibold">{masterDoc.title}</h2>
            <p>{masterDoc.plot}</p>
            <div className="flex gap-4 mt-4">
              <Button variant="outline" onClick={generateMasterDoc}>Regenerate</Button>
              <Button onClick={handleApprove}>Approve & Proceed</Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
