from openai import OpenAI
from prompts import prompt_generator as prompts
from google import genai
from google.genai import types
import config
import re
import os
import json
from io import BytesIO
from PIL import Image
from pathlib import Path
import time

# Define all relevant paths
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "output" / "thumbnails"
CACHE_PATH = OUTPUT_DIR / "prompt_cache.json"

# Ensure output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# API clients
client = OpenAI(api_key=config.OPENAI_API_KEY)
client_gemini = genai.Client(api_key=config.GEMINI_API_KEY)

def story_prompts(system_prompt, user_prompt, model="gpt-4o"):
    messages = [
        {"role": "developer", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    completion = client.chat.completions.create(model=model, messages=messages, temperature=0.2)
    return completion.choices[0].message.content

def save_thumbnail(image_data, filename):
    try:
        image = Image.open(BytesIO(image_data))
        output_path = OUTPUT_DIR / filename
        image.save(output_path)
        print(f"[✓] Image saved: {output_path}")
    except Exception as e:
        print(f"[!] Error saving image: {e}")

def generate_base_thumbnails():
    # Load master_doc
    # with open(config.MASTER_DOC_PATH, 'r') as file:
    #     master_doc_content = json.load(file)

    ## Dummy

    master_doc_content = {
  "Story Title": "When the Night Finally Speaks",
  "Author Name": "KUKU FM",
  "Story Plot": {
    "episode_1": "In the quiet village of Rosemoor, an unsettling truth has shaped generations: no one here dreams. The townsfolk have long accepted their perpetual sleep without visions—until eight-year-old Liana Willowgrove wakes from a slumber insisting she saw a vast purple sky under glowing moonlight. Word spreads quickly, crackling through the village gossip. Many dismiss Liana’s claims as childish imagination, but a few wonder if this could signal the end—or the cause—of Rosemoor’s age-old curse.\n\nEvening falls. The streets, lit only by flickering lanterns, carry a hush that feels heavier than usual. We hear a slow wind sigh through abandoned alleyways. Liana’s father, Eldon, stands outside his humble home, listening anxiously to his daughter’s excited chatter. In her soft, lilting voice, she tells him of an endless field filled with glowing spirits dancing among wild lavender. Eldon’s heart aches, torn between worry and hope. He remembers legends of dreamers and illusions from the past, all silenced by the village’s curse.\n\nYara Crispwind, a determined local teacher, visits Eldon upon hearing the rumors about Liana. She questions him over tea, her crisp manner of speaking underscoring her curiosity. Eldon confesses that Liana’s vivid descriptions have unsettled him. No one, not even elders, has experienced actual dreaming. Could Liana’s visions be a sign?\n\nAs Yara leaves, a grouchy villager named Marlow Orley confronts them. Gruff and suspicious, he warns that if the child’s stories spread, it could stir fear and chaos. Casting an accusing glance, Marlow demands Liana be quiet before she brings misfortune on them all. Eldon refuses to silence his daughter.\n\nThat night, Liana sits by a dim lantern, gazing out the window. She hears a faint whisper carried by the wind—something calling her name, urging her not to be afraid. Her heart pounds. In the darkness, the village remains silent and dreamless, except for Liana’s restless mind.\n\nJust as she closes her eyes, she sees a flicker of that purple sky. She wakes sharply and gasps. From outside her window, a midnight breeze rattles the shutters. Liana can’t know for sure, but it feels like an echo of her dream come into reality. The episode ends with her whisper: “I know what I saw… and it was calling me.”",
    "episode_2": "Recap: Young Liana Willowgrove revealed vivid dreams in a village that has never dreamt. Her father, Eldon, and the curious Yara Crispwind struggled with how to protect her from the townspeople’s fear.\n\nAs dawn breaks over Rosemoor, Eldon contemplates telling the village council about Liana’s dreams. He hopes they might find a cure for the curse. Meanwhile, a hesitant Yara stands outside the council hall—an imposing stone building that seems to hold secrets of generations past. She draws a sharp breath and steps inside.\n\nSeated around a long table are the elders, including Marlow Orley, who crosses his arms and glares. Eldon describes Liana’s midnight visions with determined calm. At first, the council members exchange uneasy looks. Then Marlow slams his fist on the table, insisting they must stifle the gossip. “This so-called dream could invite a worse evil,” he snarls. Yara challenges him, pointing out that the curse has done nothing but silence them for decades. Maybe Liana’s dream is the key to freedom.\n\nLater, Liana plays by the murmuring fountain in the village square. Children skip rocks but keep a wary distance from her as their parents watch from doorways. Whispering to herself, Liana recalls the swirl of color and warmth in her dream. Suddenly, she glimpses a flicker of movement from the corner of her eye. A faint silhouette of a tall figure draped in mist stands at the alley’s end, beckoning. When she blinks, it vanishes.\n\nThat evening, Eldon and Yara gather round Liana as she speaks hesitantly of the vision. She remembers the silhouette’s gentle voice guiding her down a hidden path in a moonlit field. Eldon, with his gentle British accent, comforts her: “We will find what’s behind this mystery, my darling.” The wind rattles the brittle shutters again, as if something beyond the walls of Rosemoor is stirring.\n\nFar off, a thunderclap echoes in the distance. Marlow skulks nearby, listening. His mistrust runs deep—he fears that Liana’s visions might summon danger. Yet even he betrays a flicker of curiosity in his usually gruff voice.\n\nNight falls, and Liana drifts into a half-sleep. We hear her breath quicken, and then she softly murmurs: “There it is again… the purple sky… the voice…” Her eyes snap open. Hope meets dread as she realizes the dream is drawing her nearer to a place she cannot resist. The episode snaps to a close as she stands at her window, the silhouette’s voice resonating with her heart: “Come… follow the moon.”",
    "episode_3": "Recap: Liana’s dream intensifies, and she catches a glimpse of a mysterious silhouette that seems to call her beyond Rosemoor’s boundaries.\n\nThe episode opens under a heavy rain. Thunder rumbles as Eldon, Yara, and Liana huddle in a candlelit parlor. They’ve decided to explore the abandoned chapel on the outskirts of the village, rumored to hold fragments of an old legend about dreaming. Yara believes that if they can piece together the curse’s origin, they might break it.\n\nMarlow Orley intercepts them at the chapel gates, clutching a lantern against the wind. “You should leave this place alone,” he growls. But Liana steps forward, determination in her small voice: “I have to see what’s inside.” Marlow grudgingly steps aside.\n\nInside, the chapel walls are lined with faded murals, their colors washed away by time. Lightning illuminates half-hidden carvings of moons and stars. The sound of rain dripping through the cracked roof punctuates the silence. Yara carefully thumbs through an ancient tome discovering references to a ‘Twilight Field,’ matching Liana’s dream description. The legend suggests a guide once led the villagers in shared dream journeys—but that connection was severed by a dark rift. The result: a village forever stripped of dreams.\n\nAs Liana lingers by a broken altar, a sudden chill wafts through the chapel. The faint outline of the mysterious silhouette appears again. In an echoing voice that only Liana can hear, it speaks: “Return to the place of beginnings… only the child of new dreams can mend what was broken.” Liana trembles, her wide eyes locked on the fading figure.\n\nShe recounts the words aloud. Eldon’s hands shake with a mix of hope and fear, while Yara’s eyes sparkle, convinced this is the key. They vow to seek an old forest clearing rumored to stand at the border of Rosemoor’s farmland—a place heavily avoided by villagers. Marlow wavers, torn between skepticism and the haunting possibility that Liana’s dream is real.\n\nAt the chapel’s threshold, thunder crashes. A gust of wind extinguishes every candle, plunging them into darkness. In the clamoring night, Eldon grips Liana’s hand, whispering: “We must find that clearing.” Through the rain, we hear Liana steady her breath, as though she’s making a silent promise. The episode ends with Marlow raising his lantern, revealing doubt etched across his face—not sure if this path leads to redemption or deeper damnation.",
    "episode_4": "Recap: After discovering ancient texts in the chapel, Liana, Eldon, Yara, and a reluctant Marlow prepare to search for the hidden clearing that may hold the fate of Rosemoor’s curse.\n\nAt dawn, the group sets out with cautious hearts. They traverse tangled forest paths where twisting branches loom overhead. Leaves rustle ominously. Occasionally, Liana halts, shutting her eyes to sense the whispering voice that leads her forward. Yara’s crisp tones reassure everyone to stay hopeful, while Marlow’s gruff mutterings betray his anxious mistrust.\n\nAs midday light filters through the canopy, they arrive at a moss-covered gate—a threshold to a clearing bathed in a mysterious hush. The air feels charged, and even the birds fall silent. Liana steps first into the open space. She recognizes the curve of the tall grass from her dreams. The sky above seems eerily still.\n\nA sudden swirl of wind sweeps the clearing, forming into the shape of that misty silhouette. In whispers that echo, it instructs them to gather around an ancient stone dais. The dais is cracked with age, covered by inscriptions that correspond to the patterns from the chapel murals. Eldon reads them aloud in a trembling voice, a half-forgotten chant that once guided villagers to a shared dreaming ceremony.\n\nThe wind howls, and a faint shimmer arcs across the clearing. Shadows rise from the corners—phantasms of past villagers, sorrow etched on their translucent faces. The air thickens with the weight of old regret and longing. Each spirit glides toward Liana, as if pleading for release from this sleepless curse.\n\nMarlow stumbles back, fear thrumming in his chest. He shouts for them to stop meddling in cursed magic. Yet Yara, her voice resolute, declares: “We’ve come this far. We can’t turn back now.” Liana steps onto the dais, swaying as the swirling apparitions brush past her. She closes her eyes, summoning the memory of her purple-sky dream. Her voice is small but resolute: “I will not abandon you.”\n\nSuddenly, the dais cracks. A column of pale light flares upward, and reality seems to quiver. A powerful gust knocks everyone off their feet. As the light dims, Liana and the silhouette vanish, leaving the clearing silent. Eldon scrambles forward, calling his daughter’s name. Echoes fade into the gloom.\n\nThe episode ends on this sudden void of sound, each character reeling from the loss. In the final moment, we hear Eldon’s panicked shout: “Liana!” as the wind dies, leaving them alone in an eerie, dream-like hush.",
    "episode_5": "Recap: At the hidden clearing, Liana vanished alongside the mysterious silhouette, leaving Eldon, Yara, and Marlow stunned and frightened.\n\nThe finale opens with Eldon kneeling on the broken dais. His voice resonates in the stillness: “Liana, come back!” A faint glimmer in the air pulls everyone’s gaze upward, revealing a soft glow at the clearing’s edge. Yara rushes toward it, Marlow in tow, lantern rattling in his grip.\n\nThey find Liana standing in a swirl of silver light, the silhouette by her side. Her eyes are closed, and she appears both peaceful and fierce, as though entirely consumed by the dream realm. In an echoing voice, the silhouette speaks through Liana: “The time to lift the curse is now. Bold hearts must share the dream.”\n\nEldon, tears mixing with relief, steps forward. He calls her name gently. Liana opens her eyes, her voice emerging stronger than ever: “Father, help me finish the chant. We must unite all the villagers in belief again.” The clearing begins to shift, revealing flickers of purple sky overhead. Yara clasps Eldon’s hand, and together they recite the half-remembered incantation from the dais.\n\nMarlow watches, breathing unevenly. At first, he only listens, fear battling reason. But seeing Liana’s fearless focus, he finally joins, his rough tone blending into the chant. One by one, the phantasms of the cursed ancestors materialize, drawn by this surge of unity. Their faces flash with something like hope.\n\nThen, in a crescendo of sound, the purple sky engulfs the clearing. Moonlight bathes everything. The dais glows fiercely; the spirits release a collective sigh, drifting upward and dissolving into starlight. A distant chorus of dreaming voices swells, as though centuries of trapped visions have finally been set free.\n\nLiana sways, exhausted, and collapses into Eldon’s arms. The silhouette lingers, then bows and dissolves into shimmering motes. For the first time, a hush blankets the clearing—not the heavy silence of fear, but a tranquil calm. The curse has broken.\n\nIn the morning, villagers awake to find themselves stirring from real dreams—memories of glowing fields, starry nights, and a child’s gentle laughter. Eldon cradles Liana, tears of joy in his eyes. Marlow, once so mistrustful, stands humbled, quietly thanking her. Yara, smiling, ushers them both home. Though the road ahead is unknown, Rosemoor’s long night is over.\n\nThe final moments fade with a dawn chorus of real, hopeful voices—echoes of dreams returned at last."
  },
  "Story Characters": [
    {
      "Name": "Liana Willowgrove",
      "Age": "8",
      "Gender": "Female",
      "Accent": "Soft, lilting child’s voice",
      "Description": "A bright, intuitive girl who suddenly begins to dream of a purple sky and unknown landscapes. Her gentle courage propels the quest to break the village curse."
    },
    {
      "Name": "Eldon Willowgrove",
      "Age": "45",
      "Gender": "Male",
      "Accent": "Gentle British accent",
      "Description": "Liana’s protective father, torn between worry and hope. He speaks calmly and methodically. Though fearful of the curse’s mysteries, he loves his daughter above all else."
    },
    {
      "Name": "Yara Crispwind",
      "Age": "30",
      "Gender": "Female",
      "Accent": "Crisp, confident British accent",
      "Description": "A determined local teacher who refuses to ignore Liana’s impossible visions. Analytical yet compassionate, she becomes a driving force in uncovering the curse’s origins."
    },
    {
      "Name": "Marlow Orley",
      "Age": "50",
      "Gender": "Male",
      "Accent": "Gruff, working-class British accent",
      "Description": "A skeptical villager who fears Liana’s dreams may invite more trouble. Initially distrustful and harsh, he slowly realizes the importance of helping lift the village’s curse."
    }
  ]
}

    # Compose prompt
    system_prompt = prompts.system_prompt
    user_prompt = prompts.user_prompt % (config.N_PROMPTS, master_doc_content)
    print("[+] Generating prompts...")

    # Query OpenAI
    # raw_response = story_prompts(system_prompt, user_prompt).strip()

    
    # # Strip markdown wrappers like ```json
    # if raw_response.startswith("```"):
    #     raw_response = raw_response.strip("`").strip("json").strip()

    # print("[DEBUG] Raw OpenAI response:\n", raw_response)

    # # Extract JSON content
    # match_json = re.search(r'\{(?:.|\n)*\}', raw_response, re.S)
    # if not match_json:
    #     print("[!] Prompt JSON error! Could not find valid JSON structure.")
    #     return

    # try:
    #     prompt_data = eval(match_json.group(0))  # Alternatively use json.loads if it's valid
    # except Exception as e:
    #     print(f"[!] Failed to parse JSON: {e}")
    #     return

    # # Save prompt JSON
    # with open(CACHE_PATH, "w", encoding="utf-8") as f:
    #     json.dump(prompt_data, f, indent=2)
    #     print(f"[✓] Saved prompt cache: {CACHE_PATH}")

    prompt_data = {
  "prompt_1": "A high-quality digital painting illustration in storybook fantasy style, showing young Liana standing in a field of lavender, gazing at a purple sky filled with glowing spirits in a dreamlike twilight meadow with distant village rooftops and faint moonlight with lit by soft purple twilight and gentle glowing orbs. The scene feels mystical and hopeful. The title text \"When the Night Finally Speaks\" is written in ornate serif font with glowing silver letters at the top center, and the author name \"KUKU FM\" appears in small, handwritten-style font in pale white at the bottom right.",
  "prompt_2": "A high-quality 4K digital painting illustration in cinematic dark fantasy style, showing Liana and Eldon holding hands near a broken chapel doorway during a thunderstorm in a dark, rain-drenched forest on the outskirts of Rosemoor with lightning flashes with soft candlelight from inside the chapel. The scene feels tense yet sacred. The title text \"When the Night Finally Speaks\" is written in bold serif font in metallic grey at the top left, and the author name \"KUKU FM\" appears in small cursive font in soft yellow at the bottom left.",
  "prompt_3": "A high-quality ink-and-watercolor blend illustration in gothic illustration style, showing Yara reading an ancient tome beside a glowing altar, while shadowy spirits loom behind her in an abandoned chapel with faded murals and cracked floors with dim candlelight and glowing ethereal light from the altar. The scene feels mysterious and reverent. The title text \"When the Night Finally Speaks\" is written in script font in crimson red at the bottom center, and the author name \"KUKU FM\" appears in clean serif font in faded gold at the top right.",
  "prompt_4": "A high-quality digital watercolor illustration in storybook surrealism style, showing a misty silhouette beckoning Liana from a moonlit forest clearing in a mossy clearing surrounded by towering trees and ghostly fog with soft blue moonlight filtered through fog. The scene feels haunting and magical. The title text \"When the Night Finally Speaks\" is written in elegant serif font in glowing violet at the top center, and the author name \"KUKU FM\" appears in simple white font in italics at the bottom left.",
  "prompt_5": "A high-quality HDR digital painting illustration in ethereal fantasy style, showing Liana surrounded by spectral villagers with hopeful eyes in a glowing circle of light in the ancient dais in the middle of a forest clearing at night with radiant silver light beaming from the dais. The scene feels uplifting and spiritual. The title text \"When the Night Finally Speaks\" is written in bold fantasy-style font in radiant gold at the top center, and the author name \"KUKU FM\" appears in thin serif in white at the bottom center.",
  "prompt_6": "A high-quality digital anime-style painting illustration in dramatic animated style, showing Eldon clutching Liana as the spirits fade into starlight around them in an open clearing under a purple starry sky with soft starlight and warm glow from below. The scene feels emotional and triumphant. The title text \"When the Night Finally Speaks\" is written in calligraphic serif in warm gold at the top center, and the author name \"KUKU FM\" appears in blocky white font in small caps at the bottom right.",
  "prompt_7": "A high-quality detailed pencil sketch with digital color overlay illustration in stylized fantasy realism style, showing Marlow, Yara, Eldon and Liana holding hands in a circle surrounded by glowing spirits in the center of the ancient clearing beneath glowing sky fractals with backlit by radiant moonbeams and soft glows. The scene feels united and reverent. The title text \"When the Night Finally Speaks\" is written in classic serif in dark silver at the top left, and the author name \"KUKU FM\" appears in small modern script in light blue at the bottom right.",
  "prompt_8": "A high-quality digital mixed media illustration in dreamlike fantasy style, showing Liana floating in a swirl of silver light, eyes closed with a serene expression in the dream realm with cosmic skies and floating lavender petals with glow from beneath and sparkles of distant stars. The scene feels peaceful and transcendent. The title text \"When the Night Finally Speaks\" is written in glowing script in silver and lavender at the top center, and the author name \"KUKU FM\" appears in delicate serif font in soft pink at the bottom left.",
  "prompt_9": "A high-quality digital painting with ink outlines illustration in storybook interior illustration style, showing Liana looking out the window as the purple sky flickers in the night in her small bedroom dimly lit by lantern glow with dim golden lantern light and flickers of purple from outside. The scene feels curious and dreamy. The title text \"When the Night Finally Speaks\" is written in storybook serif font in gold at the bottom center, and the author name \"KUKU FM\" appears in italic serif in pale orange at the top right.",
  "prompt_10": "A high-quality digital illustration in painted texture illustration in hopeful storybook realism style, showing a final sunrise over Rosemoor as villagers awaken from dreams for the first time in village rooftops glowing with morning light and drifting spirit motes with warm sunrise glow. The scene feels peaceful and joyous. The title text \"When the Night Finally Speaks\" is written in classic serif in white and gold gradient at the top center, and the author name \"KUKU FM\" appears in clean sans-serif in soft grey at the bottom center."
}

    # Generate images from prompts
    for i in range(1, config.N_PROMPTS + 1):
        prompt_key = f"prompt_{i}"
        prompt = prompt_data.get(prompt_key)
        if not prompt:
            print(f"[!] Missing prompt: {prompt_key}")
            continue

        print(f"[→] Prompt {i}: {prompt}")

        response = client_gemini.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(response_modalities=['Text', 'Image'])
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                save_thumbnail(part.inline_data.data, f"gemini-native-image_{i}.png")

        time.sleep(30)

if __name__ == "__main__":
    generate_base_thumbnails()
    
