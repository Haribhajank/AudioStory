from smallest import Smallest
client_sai = Smallest(api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2N2M1Zjc4NWZlNGVkZmExNTk3Y2VkYmQiLCJpYXQiOjE3NDQxMjM1MjR9.Qwu0gSmewo991UhhwPoYubyrNmUMoubBJYUN5X0A7ug")

text = """"I’m Calliope, the creative core of this pipeline. You give me an idea – a trope, plot, or theme – and I’ll take it from there."
Here's what I do:
I take in the core inputs: story idea or trope, number of episodes, desired A Fully Automated Audio Storytelling Engine time per episode, and the genre.
Based on this, I generate:
 - A unique story title
 - Plot outline with episodic division
 - Character personas – including Name, Age, Gender, Accent, and Description
 - Episode recaps to ensure continuity

Using this information, I build a master document. This acts as the foundation for script generation.
Then, for each episode, I sequentially generate a detailed script that fits within the chosen time limit. At the end of each episode, I summarize it into a recap. This recap becomes the context for generating the next episode — maintaining solving continuity issues and long context limits.
Users can download the scripts as PDFs, ready for review or refinement.
To bring this to life, I used the O1 model, and here’s why:
After rigorous testing against GPT-4o and O3-mini, I found that O1 consistently produced better plot arcs, richer character development, and a deeper understanding of storytelling logic.

- O3-mini, despite being tuned for reasoning, lacked depth for creative writing may be due to more geared for quantitative domain task like science and math.
- GPT-4o, while generalised, failed to outperform o1 in creative writing.

In short, O1 gave the most cinematic and coherent output showcasing great story arch understanding and continuty, making it worth the extra compute cost. A classic tradeoff between quality and cost, and we went all in for quality.
"""


client_sai.synthesize(
            text=text,
            voice_id="chirag",
            model="lightning-large",
            speed=1.0,
            sample_rate=24000,
            enhancement=2.0,
            save_as="calliope.wav"
        )