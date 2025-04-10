from django.shortcuts import render
import time

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from .serializers import (
    IdeaInputSerializer,
    EpisodeInputSerializer,
    ThumbnailPromptSerializer,
    FinalImageInputSerializer,
)
import subprocess
import json
import os
import uuid
from pathlib import Path
import traceback
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class AudioInputSerializer(serializers.Serializer):
    episode_index = serializers.IntegerField()

BASE_DIR = Path(__file__).resolve().parent.parent

@api_view(['POST'])
def generate_story(request):
    serializer = IdeaInputSerializer(data=request.data)
    if serializer.is_valid():
        idea = serializer.validated_data['idea']
        numEpisodes = serializer.validated_data["numEpisodes"]
        timePerEpisode = serializer.validated_data["timePerEpisode"]
        genre = serializer.validated_data["genre"]
        script_path = BASE_DIR.parent / 'audio_story_project/scripts/generate_master_doc.py'
        

        # 🔽 Print what's running
        print("Running:", ['python', str(script_path), idea, numEpisodes, timePerEpisode, genre])

        result = subprocess.run(['python', str(script_path), idea, numEpisodes, timePerEpisode, genre], capture_output=True, text=True)

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
        serializer = EpisodeInputSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            ep_index = serializer.validated_data["index"]
        script_path = BASE_DIR.parent / 'audio_story_project/scripts/generate_episode.py'
        print("▶️ Running:", ['python', str(script_path), ep_index])
        

        result = subprocess.run(['python', str(script_path), ep_index], capture_output=True, text=True)
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
            script_url = f"/episodes/episode_{int(ep_index)+1}.json"
            return Response({"script_url": script_url})


        print("❌ Episode folder does not exist")
        return Response({"error": "Episodes not found."}, status=500)

    except Exception as e:
        print("❌ Error in generate_episodes:", str(e))
        return Response({"error": str(e)}, status=500)



# @api_view(['POST'])
# def generate_thumbnails(request):
#     script_path = BASE_DIR.parent / 'thumnail_generation/thumnail_pipeline.py'
#     print(" Running thumbnail pipeline:", script_path)

#     result = subprocess.run(
#         ['python', str(script_path)],
#         capture_output=True,
#         text=True,
#         cwd=BASE_DIR.parent / 'thumnail_generation',
#         env={**os.environ, "PYTHONIOENCODING": "utf-8"}  
#     )

#     print(" stdout:", result.stdout)
#     print(" stderr:", result.stderr)

#     output_folder = BASE_DIR.parent / 'thumnail_generation/output/thumbnails'
#     thumbnails = []
#     if output_folder.exists():
#         for filename in sorted(os.listdir(output_folder)):
#             if filename.endswith(".png") and not filename.startswith("story_thumbnail"):
#                 url = f'/media/thumbnails/{filename}'
#                 print(" Thumbnail URL:", url)  # ✅ Add this line to print each URL
#                 thumbnails.append(url)
#         return Response({"thumbnails": thumbnails})
    
#     print(" No thumbnails found in:", output_folder)
#     return Response({"error": "Thumbnails not found."}, status=500)



# @api_view(['POST'])
# def generate_thumbnails(request):
#     script_path = settings.BASE_DIR.parent / 'thumnail_generation/generate_base_thumbnails.py'
#     output_folder = settings.BASE_DIR.parent / 'thumnail_generation/output/thumbnails'

#     logger.info(" Starting thumbnail generation via Gemini")
#     logger.debug(f"Script path: {script_path}")

#     result = subprocess.run(
#         ['python', str(script_path)],
#         capture_output=True,
#         text=True,
#         cwd=settings.BASE_DIR,
#         env={**os.environ, "PYTHONIOENCODING": "utf-8"}
#     )

#     logger.info(" Thumbnail generation script completed")
#     logger.debug(f"STDOUT:\n{result.stdout}")
#     logger.debug(f"STDERR:\n{result.stderr}")

#     thumbnails = []
#     if output_folder.exists():
#         for filename in sorted(os.listdir(output_folder)):
#             if filename.endswith(".png") and not filename.startswith("story_thumbnail"):
#                 url = f'/media/thumbnails/{filename}'
#                 thumbnails.append(url)
#                 logger.debug(f" Found thumbnail: {url}")

#         if thumbnails:
#             logger.info(f" {len(thumbnails)} thumbnails generated")
#             return Response({"thumbnails": thumbnails})
#         else:
#             logger.warning(" No valid thumbnails found.")
#             return Response({"error": "No thumbnails generated."}, status=500)

#     logger.error(f" Thumbnail output folder not found: {output_folder}")
#     return Response({"error": "Thumbnail directory missing."}, status=500)



@api_view(['POST'])
def generate_thumbnails(request):
    output_folder = BASE_DIR.parent / 'thumnail_generation/output/thumbnails'
    thumbnails = []

    
    if output_folder.exists():
        for filename in sorted(os.listdir(output_folder)):
            if filename.endswith(".png") and not filename.startswith("story_thumbnail"):
                url = f'/media/thumbnails/{filename}'
                thumbnails.append(url)

        print("[✓] Loaded existing thumbnails:", thumbnails)
        return Response({"thumbnails": thumbnails})
    

    return Response({"error": "Thumbnail folder not found."}, status=500)





# @api_view(['POST'])
# def generate_final_image(request):
#     serializer = FinalImageInputSerializer(data=request.data)
#     if serializer.is_valid():
#         index = serializer.validated_data['prompt_index']
#         prompt_key = f"prompt_{index + 1}"
#         script_path = BASE_DIR.parent / 'thumnail_generation/thumnail_pipeline.py'
#         subprocess.run(['python', str(script_path), prompt_key], capture_output=True, text=True)
#         final_image_path = BASE_DIR.parent / 'thumnail_generation/output/thumbnails/story_thumbnail.png'
#         if final_image_path.exists():
#             return Response({"image": '/media/thumbnails/story_thumbnail.png'})
#         return Response({"error": "Final thumbnail generation failed."}, status=500)
#     return Response(serializer.errors, status=400)




# @api_view(['POST'])
# def generate_final_image(request):
#     serializer = FinalImageInputSerializer(data=request.data)
#     if serializer.is_valid():
#         index = serializer.validated_data['prompt_index']
#         prompt_key = f"prompt_{index + 1}"
        
#         script_path = settings.BASE_DIR.parent / 'thumnail_generation' / 'generate_final_image.py'
#         final_image_path = settings.BASE_DIR.parent / 'thumnail_generation' / 'output' / 'thumbnails' / 'story_thumbnail.png'

#         logger.info(f"Starting final thumbnail generation using Imagen for {prompt_key}")
#         logger.debug(f"Script path: {script_path}")

#         result = subprocess.run(
#             ['python', str(script_path), prompt_key],
#             capture_output=True,
#             text=True,
#             cwd=str(script_path.parent),  # Set working dir to script directory
#             env={**os.environ, "PYTHONIOENCODING": "utf-8"}
#         )

#         logger.info("Final image generation script completed")
#         logger.debug(f"STDOUT:\n{result.stdout}")
#         logger.debug(f"STDERR:\n{result.stderr}")

#         if final_image_path.exists():
#             logger.info(f"Final image saved at: {final_image_path}")
#             return Response({"image": '/media/thumbnails/story_thumbnail.png'})
#         else:
#             logger.error("Final image not found after script execution.")
#             return Response({"error": "Final thumbnail generation failed."}, status=500)

#     logger.error(f"Serializer error: {serializer.errors}")
#     return Response(serializer.errors, status=400)





@api_view(['POST'])
def generate_final_image(request):
    final_image_path = BASE_DIR.parent / 'thumnail_generation/output/thumbnails/story_thumbnail.png'

    if final_image_path.exists():
        return Response({"image": "/media/thumbnails/story_thumbnail.png"})
    
    return Response({"error": "Final thumbnail not found."}, status=500)


# @api_view(['POST'])
# def generate_audio(request):
#     serializer = AudioInputSerializer(data=request.data)
#     if serializer.is_valid():
#         try:
#             episode_index = serializer.validated_data['episode_index']
#             script_id = str(uuid.uuid4())[:8]

#             input_path = BASE_DIR.parent / f"audio_story_project/data/episodes/episode_{episode_index + 1}.json"
#             output_path = BASE_DIR.parent / f"AudioGeneration/output/episode_{script_id}.wav"

#             print(f"[DEBUG] Input Path: {input_path}")
#             print(f"[DEBUG] Output Path: {output_path}")

#             if not input_path.exists():
#                 return Response({"error": f"Episode file not found: episode_{episode_index + 1}.json"}, status=404)

#             script_path = BASE_DIR.parent / 'AudioGeneration/audio_pipeline.py'
#             print(f"[DEBUG] Running script: {script_path}")

#             result = subprocess.run(
#                 ['python', str(script_path), str(input_path), str(output_path)],
#                 capture_output=True,
#                 text=True
#             )

#             print("[STDOUT]:", result.stdout)
#             print("[STDERR]:", result.stderr)

#             if output_path.exists():
#                 return Response({"audio_url": f"/audio/{output_path.name}"})


#             print("[ERROR] Output audio file was not created.")
#             return Response({"error": "Audio generation failed."}, status=500)

#         except Exception as e:
#             traceback.print_exc()
#             return Response({"error": "Internal server error."}, status=500)

#     return Response(serializer.errors, status=400)

#################################################################################################################


@api_view(['POST'])
def generate_audio(request):
    serializer = AudioInputSerializer(data=request.data)
    if serializer.is_valid():
        try:
            episode_index = serializer.validated_data['episode_index']
            
            # 🎯 Use a fixed dummy script_id to point to an existing file
            dummy_script_id = "a2f7e49e"
            output_path = BASE_DIR.parent / f"AudioGeneration/output/episode_{dummy_script_id}.wav"
          

            print(f"[DEV MODE] Skipping audio generation. Looking for: {output_path}")

            if output_path.exists():
                return Response({"audio_url": f"/audio/{output_path.name}"})

            return Response(
                {"error": f"Dummy audio not found at {output_path}"},
                status=404
            )

        except Exception as e:
            traceback.print_exc()
            return Response({"error": "Internal server error."}, status=500)

    return Response(serializer.errors, status=400)
