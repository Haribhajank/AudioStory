from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    IdeaInputSerializer,
    EpisodeInputSerializer,
    ThumbnailPromptSerializer,
    FinalImageInputSerializer,
    AudioInputSerializer
)
import subprocess
import json
import os
import uuid
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

@api_view(['POST'])
def generate_story(request):
    serializer = IdeaInputSerializer(data=request.data)
    if serializer.is_valid():
        idea = serializer.validated_data['idea']
        script_path = BASE_DIR.parent / 'audio_story_project/scripts/generate_master_doc.py'
        


        # 🔽 Print what's running
        print("Running:", ['python', str(script_path), idea])

        result = subprocess.run(['python', str(script_path), idea], capture_output=True, text=True)

        # 🔽 Show the output and error (critical!)
        print("stdout:", result.stdout) 
        print("stderr:", result.stderr)

        output_file = BASE_DIR.parent / 'audio_story_project/data/master_doc.json'
        print("Looking for master_doc at:", output_file)
        if output_file.exists():
            print(" master_doc.json found!")
            with open(output_file) as f:
                doc = json.load(f)
            return Response(doc)
        else:
            print(" master_doc.json not found after script run.")

        return Response({"error": "Failed to generate master doc."}, status=500)

    return Response(serializer.errors, status=400)

@api_view(['POST'])
def generate_episodes(request):
    try:
        script_path = BASE_DIR.parent / 'audio_story_project/scripts/generate_episode.py'
        print("▶️ Running:", ['python', str(script_path), "3"])

        result = subprocess.run(['python', str(script_path), "3"], capture_output=True, text=True)
        print("📤 stdout:", result.stdout)
        print("📥 stderr:", result.stderr)

        output_folder = BASE_DIR.parent / 'audio_story_project/data/episodes'
        print("🔍 Looking in:", output_folder)

        episodes = []
        if output_folder.exists():
            for filename in sorted(os.listdir(output_folder)):
                if filename.endswith(".json"):
                    with open(output_folder / filename) as f:
                        episodes.append(json.load(f))
            print(f"✅ {len(episodes)} episodes loaded")
            return Response({"episodes": episodes})

        print("❌ Episode folder does not exist")
        return Response({"error": "Episodes not found."}, status=500)

    except Exception as e:
        print("❌ Error in generate_episodes:", str(e))
        return Response({"error": str(e)}, status=500)



@api_view(['POST'])
def generate_thumbnails(request):
    # No need to validate or extract title/plot anymore
    script_path = BASE_DIR.parent / 'thumnail_generation/thumnail_pipeline.py'
    print(" Running thumbnail pipeline:", script_path)

    result = subprocess.run(
        ['python', str(script_path)],
        capture_output=True,
        text=True,
        cwd=BASE_DIR.parent / 'thumnail_generation',
        env={**os.environ, "PYTHONIOENCODING": "utf-8"}  
    )

    print(" stdout:", result.stdout)
    print(" stderr:", result.stderr)

    output_folder = BASE_DIR.parent / 'thumnail_generation/output/thumbnails'
    thumbnails = []
    if output_folder.exists():
        for filename in sorted(os.listdir(output_folder)):
            if filename.endswith(".png") and not filename.startswith("story_thumbnail"):
                thumbnails.append(f'/media/thumbnails/{filename}')
        return Response({"thumbnails": thumbnails})
    return Response({"error": "Thumbnails not found."}, status=500)



@api_view(['POST'])
def generate_final_image(request):
    serializer = FinalImageInputSerializer(data=request.data)
    if serializer.is_valid():
        index = serializer.validated_data['prompt_index']
        prompt_key = f"prompt_{index + 1}"
        script_path = BASE_DIR / 'thumbnail_generation/thumnail_pipeline.py'
        subprocess.run(['python', str(script_path), prompt_key], capture_output=True, text=True)
        final_image_path = BASE_DIR / 'thumnail_generation/output/thumbnails/story_thumbnail.png'
        if final_image_path.exists():
            return Response({"image": '/media/thumbnails/story_thumbnail.png'})
        return Response({"error": "Final thumbnail generation failed."}, status=500)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def generate_audio(request):
    serializer = AudioInputSerializer(data=request.data)
    if serializer.is_valid():
        script_text = serializer.validated_data['script']
        script_id = str(uuid.uuid4())[:8]
        input_path = BASE_DIR / f"audio_story_project/data/episodes/episode_{script_id}.json"
        output_path = BASE_DIR / f"AudioGeneration/output/episode_{script_id}.wav"

        os.makedirs(input_path.parent, exist_ok=True)
        with open(input_path, "w") as f:
            f.write(script_text)

        script_path = BASE_DIR / 'AudioGeneration/audio_pipeline.py'
        subprocess.run(['python', str(script_path), str(input_path), str(output_path)], capture_output=True, text=True)

        if output_path.exists():
            return Response({"audio_url": f"/media/audio/ep_{script_id}.mp3"})
        return Response({"error": "Audio generation failed."}, status=500)
    return Response(serializer.errors, status=400)
