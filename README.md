# 🌐 English to Kham Translator

I built this because I wanted to preserve something beautiful that's slowly fading away.

Kham is a Tibeto-Burman language spoken in the remote hills of Nepal, and honestly? Most people have never heard of it. That bothered me. Languages carry entire worlds—stories, humor, ways of seeing things that just don't translate. When a language disappears, we lose all of that. when someone says that i am magar they assume that i speak magar but i dont speak magar language i speak kham. Not every magar speak same language. The langauge differ from the place where they live.

So here's a simple web app that lets you look up English words and find their Kham equivalents. Nothing fancy, just a clean interface that does one thing well.

## Why I Made This (and the choices I had to make)

Initially, I thought about building this as a full-blown React app with a backend API. Overkill. Seriously. I realized I was overengineering because that's what I'm comfortable with, not because the project needed it.

**Streamlit saved me weeks of work.** I know some developers look down on it as "not real development," but that's nonsense. It let me focus on the actual problem making Kham accessible instead of wrestling with state management and API endpoints. The whole thing came together in a weekend.

The dictionary itself (`kham_index.json`) has around 3,000+ entries. I wish it had more, but that's what I could compile from available resources. It's a start.

## What Actually Works

**The search is smarter than it looks.** Type "hap" and it'll find "happy." Type "TREE" and it'll find "tree." Case doesn't matter, and partial matches work too. I added fuzzy matching using Python's `difflib` because people make typos—I certainly do. If you search for "hapiness" (missing the 'p'), it'll suggest "happiness."

**The UI is deliberately minimal.** I tried adding animations, gradients, and all that flashy stuff at first. It looked like a 2015 Bootstrap template threw up on the screen. So I stripped it back. Clean, centered, focused. Sometimes less really is more.

**It caches the dictionary on load** using Streamlit's `@st.cache_data`. Loading a 178KB JSON file on every keystroke would be stupid, so this was non-negotiable.

## Trade-offs I Made (and why)

**No database.** Just a JSON file. Could I have used PostgreSQL or MongoDB? Sure. Would it make the app better? Not really. The dictionary is static, the file is small, and JSON loads in milliseconds. Adding a database would've meant deployment complexity, connection pooling, migrations... for what? To feel like a "real" developer? Pass.

**No user accounts or history.** I thought about adding "recently searched words" or "favorites," but that meant cookies, storage, privacy considerations. The app is stateless by design. You search, you get results, done. It's liberating, actually.

**Deployed on Streamlit Cloud (probably).** I could've Dockerized this and thrown it on AWS with a custom domain. But Streamlit Cloud is free, deploys in 30 seconds, and handles SSL automatically. I'm not trying to impress anyone with my DevOps skills here.

## How to Run This Thing

You'll need Python 3.7 or higher. That's it.

```bash
# Clone it
git clone <your-repo-url>
cd Kham

# Install dependencies (just Streamlit, really)
pip install -r requirements.txt

# Run it
streamlit run app.py
```

Or if you're on Windows and don't want to type commands, just double-click `run_app.bat`. I added that because my non-technical friends wanted to try it.

## Known Issues (because honesty matters)

- **The dictionary is incomplete.** Some common words are missing. I'm working on it.
- **No pronunciation guide.** I don't know how to pronounce half these words myself, so I can't in good conscience add phonetic guides yet.
- **Suggestions can be weird.** The fuzzy matching sometimes suggests words that make no sense. It's using a 0.6 similarity cutoff, which is... arbitrary. I picked it because it felt right.

## Contributing

If you speak Kham or know someone who does, please reach out. I need help expanding the dictionary and verifying translations. This project is bigger than me.

## Final Thoughts

This isn't a perfect app. It's not even a great app. But it's a working app that does something meaningful—it makes a rare language a little more accessible. And sometimes, that's enough.

If you use this and find it helpful, or if you have suggestions, let me know. I'm still figuring this out as I go.

---

*Built with Streamlit, caffeine, and a genuine desire to preserve something worth saving.*
