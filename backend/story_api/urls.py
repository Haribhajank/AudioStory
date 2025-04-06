from django.urls import path
from .views import (
    generate_story,
    generate_episodes,
    generate_thumbnails,
    generate_final_image,
    generate_audio
)

urlpatterns = [
    path('story/', generate_story),
    path('episodes/', generate_episodes),
    path('thumbnails/', generate_thumbnails),
    path('final-image/', generate_final_image),
    path('audio/', generate_audio),
]
