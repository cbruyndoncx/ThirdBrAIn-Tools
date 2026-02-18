# Nano Banana Golden Rules

Google's official guide for prompting Gemini's image generation. Use this when helping users write or improve prompts.

## The Four Golden Rules

### Rule 1: Edit, Don't Re-roll

If an image is 80% correct, ask for specific changes instead of starting over.

**Why it works:** Gemini is a thinking model. Continuing the conversation gives it more context to work with. The session remembers prior thoughts, yielding more consistent updates.

**Example:**
- ❌ "Generate a new coffee shop scene" (loses context)
- ✅ "Make the lighting warmer and add steam rising from the cup" (iterates)

---

### Rule 2: Use Natural Language & Full Sentences

Brief it like you would a human artist, not "tag soup."

**Tag soup (old style):**
```
cat, orange tabby, sitting, window, sunlight, cozy, warm lighting, 8k, hyperrealistic, bokeh
```

**Natural language (preferred):**
```
An orange tabby cat sitting on a windowsill, bathed in warm afternoon sunlight. The scene feels cozy and intimate, with soft focus on the background.
```

**Why it works:** Gemini was trained on natural language. Both can produce good results, but natural language is easier - no special syntax to memorize.

---

### Rule 3: Be Specific and Descriptive

Define the subject, setting, lighting, mood, textures, materials - go deep.

**Vague:**
```
A person in a coffee shop
```

**Specific:**
```
A young woman in her late 20s sitting at a weathered wooden table in a sun-drenched corner of an artisan coffee shop. Warm morning light streams through large industrial windows, casting long shadows across her laptop. She wears a cream wool sweater, her dark hair loosely gathered. A ceramic cup of cortado sits beside her, wisps of steam catching the light. The exposed brick walls are adorned with vintage botanical prints. The mood is peaceful, focused, contemplative.
```

**Why it works:** Gemini can handle A LOT of description. Don't hold back - the model is surprisingly consistent even with very detailed prompts.

---

### Rule 4: Provide Context

Tell the "why" or "for whom" so the model makes smarter creative choices.

**Without context:**
```
A portrait of a young professional
```

**With context:**
```
A portrait of a young professional for a luxury watch brand advertisement - should feel aspirational, confident, with dramatic studio lighting
```

**Why it works:** Context influences aesthetic choices. A portrait "for a children's book" looks very different from one "for a luxury brand."

**Context examples:**
- "for a tech startup landing page"
- "for a children's book illustration"
- "for a vintage poster design"
- "for a luxury brand advertisement"
- "for a SaaS pitch deck hero image"

---

## Comparison Demos

When teaching these rules, generate parallel versions so users can see the difference:

1. **Rule 2 demo:** Tag soup vs natural language (same concept)
2. **Rule 3 demo:** Vague vs detailed (same subject)
3. **Rule 4 demo:** No context vs with context (same scene)

Name outputs descriptively: `concept_tag_soup.png` vs `concept_natural_language.png`

---

## Quick Reference

| Rule | Principle | Key Phrase |
|------|-----------|------------|
| 1 | Edit, don't re-roll | "Change X" not "Generate new" |
| 2 | Natural language | "Talk to it like a designer" |
| 3 | Be specific | "Layer in the details" |
| 4 | Provide context | "Tell it the why" |
