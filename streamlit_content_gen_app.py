# streamlit_content_gen_app.py
# To run: streamlit run streamlit_content_gen_app.py

import re
import streamlit as st
import openai

# --------------- Brand Tone Dictionary ---------------
brand_tones = {
    "Cotton On": (
        "Cotton On's tone speaks to Gen Z with a casual, playful, and inclusive voice. "
        "It's real, friendly, and direct — like talking to a mate, not a brand.\n\n"
        "💬 Tone of Voice:\n"
        "- Casual\n"
        "- Friendly\n"
        "- Real\n"
        "- Conversational\n"
        "- Inclusive\n"
        "- Authentic\n"
        "- Playful\n"
        "- Clever\n"
        "- Optimistic but grounded\n"
        "- Not corporate, not fluffy, not silly\n\n"
        "🛠️ Style Guidelines:\n"
        "- Use active voice\n"
        "- Keep it punchy and scroll-stopping\n"
        "- Talk like a friend, not a brand\n"
        "- Be cheeky, but never foolish\n"
        "- Avoid lectures, jargon, and overused slang\n"
        "- Turn product features into feel-good facts\n"
        "- Light on Aussie slang, but proudly Australian\n"
        "- Make everyone feel seen, included, and heard\n"
        "- Sound like a real human — never scripted\n"
        "- Be a voice, not background noise\n\n"
        "🎯 Writing Goals:\n"
        "- Build connection, not just communication\n"
        "- Be relatable and purpose-driven\n"
        "- Reflect Gen Z values: realness, community, expression\n"
        "- Convert utility into personality (e.g. product features into benefits)\n\n"
        "📌 Example:\n"
        "Prompt: Describe a pair of oversized jeans.\n"
        "Output: Our oversized jeans hit different. Roomy, comfy, and made to move with you — not against you. "
        "Wear ‘em your way, all day."
    ),
    "Cotton On Kids": (
        "Cotton On Kids is a global fashion brand that makes everyday moments more fun. "
        "From little leaps to first steps, we design playful, easy pieces made for movement, mess, and magic. "
        "We're the cool kids of kids' fashion — bringing joy, style, and comfort to families everywhere.\n\n"
        "💬 Tone of Voice:\n"
        "- Witty\n"
        "- Fun\n"
        "- Playful\n"
        "- Warm\n"
        "- Soft\n"
        "- Familiar\n"
        "- Safe\n"
        "- Supportive\n"
        "- Imaginative\n"
        "- Comforting\n"
        "- Cheerful\n"
        "- Non-judgemental\n\n"
        "🛠️ Style Guidelines:\n"
        "- Speak with warmth and light humour\n"
        "- Use vivid, playful language that sparks imagination\n"
        "- Always write from a parent-supportive point of view\n"
        "- Be empathetic to the ups and downs of parenting\n"
        "- Keep language soft, safe, and familiar\n"
        "- Use analogies and imagery rooted in childhood play and magic\n"
        "- Avoid judgmental or 'perfect parent' tones — celebrate the messy, beautiful reality\n"
        "- Offer practical help with a wink and a smile\n"
        "- Always make the child the hero of the moment\n"
        "- Use clear, rhythmic language that's fun to read aloud\n\n"
        "📌 Example:\n"
        "Prompt: Introduce a new range of printed pyjamas for toddlers.\n"
        "Output: Meet the pyjamas made for dreamland adventures. Soft, snuggly, and covered in prints that make bedtime feel like playtime. "
        "Because when the day ends in dinosaurs, rainbows, or rocket ships — getting ready for bed is actually fun."
    ),
    "Cotton On Body": (
        "Cotton On Body is *that* girl — confident, cool, and effortlessly real. From yoga sets to bikinis to wellness tips, "
        "we’re all about what looks good, feels good, and actually matters. We're the bestie in the changeroom who hypes you up "
        "(and tells you when your tights are see-through). Everything we say and do is about helping her feel seen, supported, and totally herself.\n\n"
        "📍 Brand Positioning:\n"
        "The go-to for activewear, intimates, swim, loungewear, and wellness – designed for real life and real bodies.\n\n"
        "💬 Tone of Voice:\n"
        "- Confidently cool\n"
        "- Effortless\n"
        "- Real\n"
        "- Cheeky\n"
        "- Uplifting\n"
        "- Conversational\n"
        "- Approachable\n"
        "- Softly hot\n"
        "- Hype-girl energy\n"
        "- Grounded when it matters\n\n"
        "🛠️ Style Guidelines:\n"
        "- Speak like a best friend who keeps it real and hypes you up\n"
        "- Use clear, positive language — never vague or fluffy\n"
        "- Keep it light, fun, and to the point\n"
        "- Use internet culture subtly — never forced or try-hard\n"
        "- Be cheeky when it counts, grounded when it matters\n"
        "- Show Aussie spirit without overdoing the slang\n"
        "- Always make her feel seen, supported, and celebrated\n"
        "- Speak on causes with purpose, clarity, and motivation — never preachy\n\n"
        "📌 Example:\n"
        "Prompt: Announce a new drop of everyday activewear sets.\n"
        "Output: Move like you mean it 💪  Our new everyday activewear just landed — made to fit, flatter and feel like your second skin. "
        "You’ll want to live in these (and probably will)."
    ),
    "Factorie": (
        "Factorie is a youth street fashion brand with a bold, confident edge. "
        "We speak directly to our Gen Z audience in a way that's cheeky, fun, and real—never cringe, never try-hard. "
        "Our content is short, sharp, and always in the know with trending TikTok slang, emojis, and the cultural pulse of our community. "
        "We serve customers across Australia and South Africa, with inclusive, culturally-aware messaging that brings everyone into the convo.\n\n"
        "💬 Tone of Voice:\n"
        "- Gen Z\n"
        "- Cheeky\n"
        "- Effortless\n"
        "- Authentic\n"
        "- Playful\n"
        "- Optimistic\n"
        "- Straight to the point\n"
        "- Not fluffy\n"
        "- Not controversial\n"
        "- Never try-hard\n\n"
        "🛠️ Style Guidelines:\n"
        "- Use Gen Z slang and trending TikTok language (when relevant)\n"
        "- Keep copy short — less is more\n"
        "- Use emojis where it feels natural\n"
        "- Be bold, but not offensive\n"
        "- Write like you’re texting a close friend\n"
        "- Avoid sounding corporate or overly polished\n"
        "- Prioritise inclusion and cultural sensitivity (especially across AU & ZA)\n"
        "- Make space for community voices — youth supporting youth\n"
        "- Sound current, confident, and always a little cheeky\n\n"
        "📌 Example:\n"
        "Prompt: Announce a new drop of oversized graphic tees.\n"
        "Output: Big fit energy 💥 Just dropped: oversized graphic tees that slap harder than your For You page. Get in quick 👀"
    ),
    "Rubi": "Rubi believes no outfit is complete without the finishing touches...",
    "Typo": (
        "Typo is a stationery, gifting, and lifestyle brand that adds personality to the everyday. "
        "We design creative, original, and a little unexpected products that encourage self-expression. "
        "Our range includes stationery, gifting items, travel accessories, home décor, and exclusive collab merchandise.\n\n"
        "💡 Brand Promise: Your space to create, play and plan\n"
        "🎯 Brand Purpose: To design products that bring happiness to your everyday\n"
        "🏷️ Positioning: Anything but ordinary, helping you be extraordinary\n"
        "🧬 Brand DNA:\n"
        "- Creative\n"
        "- Playful\n"
        "- Original\n"
        "- Great value\n\n"
        "💬 Tone of Voice:\n"
        "- Expressive\n"
        "- Fun\n"
        "- A little rebellious\n"
        "- Positive\n"
        "- Creative\n"
        "- Casual\n"
        "- Thoughtful\n\n"
        "🛠️ Style Guidelines:\n"
        "- Use clear, friendly language with personality\n"
        "- Be playful, but not chaotic\n"
        "- Celebrate individuality and creativity\n"
        "- Keep it light but purposeful\n"
        "- Avoid being too polished or formal\n"
        "- Let the product speak with a spark of surprise\n\n"
        "📌 Example:\n"
        "Prompt: Describe a new Typo journal for creative planning.\n"
        "Output: Meet your new go-to journal. With bold pages and space to dream big (or doodle small), "
        "it’s made for plans, lists, and a little creativity on the side."
    ),
    "Suprè": (
        "Suprè is your number one destination for on-trend fashion for 16–20 year olds, with core product focuses on denim and utility bases "
        "with amazing fashion tops, dresses, and the best basics at a great price point. Our edge is our gloss factor and owning the power of "
        "femininity with a cool confidence. We love listening to our customer and are focused on standing for inclusivity, embracing diversity, "
        "and empowering our community. We believe in being a brand with purpose through clear social and environmental actions.\n\n"
        "💬 Tone of Voice:\n"
        "- Confident\n"
        "- Feminine\n"
        "- Trendy\n"
        "- Inclusive\n"
        "- Empowering\n\n"
        "🧭 Values:\n"
        "- Inclusivity\n"
        "- Diversity\n"
        "- Purpose-driven\n"
        "- Empowerment\n"
        "- Social responsibility\n\n"
        "🎯 Focus:\n"
        "- Target audience: 16–20 year olds\n"
        "- Product focus: Denim; Utility-based items; Fashion tops; Dresses; Basics at a great price point\n"
        "- Brand edge: Gloss factor; Feminine power with cool confidence\n"
    ),
    "Ceres Life": (
        "Ceres Life speaks to women navigating changing bodies, evolving style, and busy lives. "
        "Our tone is warm, honest, and grounded. We support her with effortless style, responsible fashion, "
        "and thoughtful, real-world solutions. We value clarity, empathy, and authentic connection.\n\n"
        "💬 Tone of Voice:\n"
        "- Warm\n"
        "- Honest\n"
        "- Relatable\n"
        "- Conversational\n"
        "- Never corporate\n"
        "- Confident but not pushy\n"
        "- Grounded in reality\n"
        "- Kind\n"
        "- Empowering\n"
        "- Purposeful\n"
        "- Not overly casual\n"
        "- Not trend-driven\n"
        "- Community-minded\n\n"
        "🛠️ Style Guidelines:\n"
        "- Use clear, benefit-led language\n"
        "- Sound like a trusted friend with a strong sense of style\n"
        "- Explain the 'why' behind products (fit, feel, function)\n"
        "- Speak with empathy and practicality\n"
        "- Avoid greenwashing — speak to sustainability in a grounded, accessible way\n"
        "- Provide solutions, not just inspiration\n"
        "- Be informative and supportive, not salesy\n"
        "- Talk about real-life context: career, family, wellness, travel\n"
        "- Offer styling advice and real-life versatility\n"
        "- Use calm confidence — never hype or exaggeration\n\n"
        "📌 Example:\n"
        "Prompt: Introduce a sustainably made knit dress.\n"
        "Output: Made from soft, breathable cotton with a hint of stretch, this knit dress moves with you. "
        "Designed to fit and flatter through every season of life, it’s the piece you’ll keep reaching for — "
        "effortless, elevated, and made with care."
    )
}

# --------------- Markdown to HTML Converter ---------------
def markdown_to_html(text: str) -> str:
    lines = text.splitlines()
    html_lines = []
    paragraph_lines = []

    def flush_paragraph():
        nonlocal paragraph_lines
        if paragraph_lines:
            html_lines.append("<p>" + "<br>\n".join(paragraph_lines) + "</p>")
            paragraph_lines = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            continue

        m_h2 = re.match(r"^## (.+)$", stripped)
        m_h3 = re.match(r"^### (.+)$", stripped)
        m_h4 = re.match(r"^#### (.+)$", stripped)

        if m_h2:
            flush_paragraph()
            heading_text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", m_h2.group(1))
            html_lines.append(f"<h2>{heading_text}</h2>")
            continue
        if m_h3:
            flush_paragraph()
            heading_text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", m_h3.group(1))
            html_lines.append(f"<h3>{heading_text}</h3>")
            continue
        if m_h4:
            flush_paragraph()
            heading_text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", m_h4.group(1))
            html_lines.append(f"<h4>{heading_text}</h4>")
            continue

        line_html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", stripped)
        paragraph_lines.append(line_html)

    flush_paragraph()
    return "<html><body>\n" + "\n".join(html_lines) + "\n</body></html>"

# --------------- UI ---------------
st.set_page_config(page_title="Brand-Aware SEO Content Generator", page_icon="📝", layout="wide")
st.title("📝 Brand‑Aware SEO Content Generator")
st.caption("Generate SEO‑friendly titles, meta descriptions, and page copy in brand tone.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", help="Your API key is used only for this session.")
    brand = st.selectbox("Brand", list(brand_tones.keys()))
    model = st.selectbox("Model", ["gpt-5", "gpt-4o", "gpt-4.1", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"], index=0)
    word_pref = st.radio("Length (soft preference)", options=[750, 1000, 1500], index=1, format_func=lambda x: {750:"Short (~750)",1000:"Medium (~1000)",1500:"Long (~1500)"}[x])

col1, col2 = st.columns(2)
with col1:
    primary = st.text_input("Primary Keyword*", help="Required.")
    category = st.text_input("Page Category*", help="Required. E.g., 'Women's Lingerie'")
    extra_context = st.text_area("Extra Context (Optional)", placeholder="Optional: campaign goals, audience insight, seasonal trend, product USP, content angle, etc.", height=100)
with col2:
    secondary = st.text_input("Secondary Keywords (comma‑separated)")
    num_topics = st.number_input("Number of Topics", min_value=0, max_value=10, value=3, step=1)

topic_inputs = []
for i in range(int(num_topics)):
    topic_inputs.append(st.text_input(f"Topic {i+1}", key=f"topic_{i+1}"))

st.markdown("---")
generate = st.button("🚀 Generate Content", use_container_width=True)

# --------------- Generation Logic ---------------
if generate:
    if not api_key or not primary or not category:
        st.error("Please provide your API key, Primary Keyword, and Page Category.")
    else:
        topics = [t.strip() for t in topic_inputs if t and t.strip()]
        brand_tone = brand_tones.get(brand, "")

        prompt = f"{brand_tone}\n\n"
        if extra_context.strip():
            prompt += (
                "🧭 Context to guide the writing (must be reflected throughout):\n"
                f"{extra_context.strip()}\n\n"
                "Every section should explicitly connect to this context with examples, angles, or language choices.\n\n"
            )

        prompt += (
            f"Write SEO content for the page category '{category}' for the brand '{brand}'.\n\n"
            "Your task:\n"
            f"1. Create a punchy, SEO-optimized **Page Title** using the primary keyword: '{primary}'.\n"
            f"2. Suggest a strong **Meta Description** under 160 characters that includes secondary keywords: {secondary}.\n"
            "3. Write comprehensive, SEO-friendly content with a friendly intro paragraph (no heading) and sections covering each topic.\n"
            "4. Ensure the content is informative, valuable, and fully answers each topic.\n"
            "5. Let depth be driven by relevance to the provided context—do **not** pad for length. Be concise when possible; expand only when helpful.\n"
            "6. Write naturally with no bullet points or lists; use normal paragraphs only.\n"
        )

        if word_pref:
            prompt += (
                f"\nLength preference (soft): Aim roughly around {word_pref} words for the main content if the context warrants it; "
                "otherwise keep it as short as possible while being complete.\n"
            )

        if topics:
            prompt += (
                "\nStructure the content as follows:\n"
                "- Start with an intro paragraph tied to the Extra Context.\n"
                "- Then provide sections with these headings:\n"
            )
            headings = ["##", "###", "####"]
            for i, topic in enumerate(topics):
                prefix = headings[i] if i < len(headings) else "####"
                prompt += f"{prefix} {topic} — Connect this topic clearly back to the Extra Context.\n"

        try:
            client = openai.OpenAI(api_key=api_key)
            with st.spinner("Generating..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}]
                )
            generated = response.choices[0].message.content or ""
        except Exception as e:
            st.error(f"OpenAI error: {e}")
            st.stop()

        content_only = re.sub(r'(?i)(title|meta description):.*', '', generated)
        word_count = len(re.findall(r'\b\w+\b', content_only))

        st.success("Done!")
        st.caption(f"Word count (reference only): {word_count}")
        st.markdown("### Generated Content")
        st.markdown(generated)

        # Downloads
        html_output = markdown_to_html(generated)
        st.download_button("📥 Download HTML", data=html_output, file_name="generated_content.html", mime="text/html")
        st.download_button("📥 Download Markdown", data=generated, file_name="generated_content.md", mime="text/markdown")
