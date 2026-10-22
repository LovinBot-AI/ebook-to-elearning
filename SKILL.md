---
name: ebook-to-elearning
description: Trọn gói làm khoá e-learning cho chuyên gia, giảng viên, nhà đào tạo: thiết kế khoá bài bản TRƯỚC KHI quay video — hỏi đáp gom ý tưởng và tư liệu sẵn có, chọn đối tượng và trọng tâm (thuần kỹ thuật / người mới / trung lập / cả hai), áp framework thiết kế bài giảng (Backward Design, Bloom, Action Mapping, Gagné, Merrill, Mayer), lập dàn ý + phác thảo để duyệt, rồi mới biên soạn ebook e-learning đầy đủ (chương, mindmap tương tác, bộ prompt, case study, thuật ngữ, giáo án) và bộ tư liệu quay video một mạch 3–4 giờ. Sau đó (hỏi trước) đẩy repo lên GitHub Pages có mật khẩu, và tách bản FREE (mindmap, case, ebook rút gọn) cho workshop miễn phí thu lead dẫn về landing page e-learning. Sau khi quay: hướng dẫn dán video (Zoom mp4 + transcript), nối sang video-to-elearning (dò mốc theo kịch bản, thumbnail, bài mẫu, render bộ bài học), kết nối Mux (MCP + token), hỏi xác nhận rồi đăng Mux qua mux-publisher và gắn video ngược vào ebook. Dùng khi người dùng nói "lên dàn ý khoá học", "soạn ebook cho elearning", "chuẩn bị nội dung trước khi quay", "thiết kế bài giảng", "làm mindmap khoá học", "biên soạn giáo trình", "từ ebook ra elearning", "ebook to elearning", "bản free cho workshop", "lead magnet", kể cả khi không nhắc tên skill.
---

# ebook-to-elearning

CLI: `python3 ~/.claude/skills/ebook-to-elearning/bin/e2e.py <command>` (written `e2e` below).
User guide (Vietnamese): [HUONG-DAN.md](HUONG-DAN.md). Process + rationale: [docs/QUY-TRINH.md](docs/QUY-TRINH.md).
Talk to the user in Vietnamese. The rules below are in English on purpose — follow them exactly.

The video is recorded LAST, in one 3–4 hour take. Everything this skill produces exists so the speaker walks into that recording fully prepared: outline, detailed mindmap, prompts, case studies, glossary, run-of-show. **No slides** at this stage.

## ▶ START HERE — every new conversation

1. Run `e2e start` (add the project dir if one exists: `e2e start <dir>`). It lists what is missing — companion skills, Python packages, Chrome, Node, video tools, Mux connection — and for each item says what the USER does (👉) and what YOU do (🤖).
2. Tell the user, in plain Vietnamese, only what matters now: "Cần ngay" items first; "cần ở bước sau" items in one short line ("phần cắt video/đăng Mux sẽ cần cài thêm X, tôi sẽ hỏi khi tới bước đó"). Offer to set up everything at once if they prefer.
3. Missing Python packages → ask, then `pip install -r engine/requirements.txt`. Never install anything without a yes.
4. **Lazy video tools:** do NOT download the video companions (video-to-elearning, mux-publisher) or video tools (FFmpeg, Whisper ~1.6 GB, Remotion ~340 MB) until the project reaches the video step (G8) — or the user explicitly asks to set everything up now. At start, just mention in one line that the video step will need extra downloads later (~0.5–2 GB; Whisper not needed with a Zoom .vtt transcript).
5. Then continue at the step `e2e next <dir>` reports (new user → G0 intake).

**Always end every reply with ONE line:** `👉 Việc tiếp theo của bạn: …` — a concrete action in plain words (answer these questions / read X and say "duyệt" / drop the video into `quay-video/` / create a Mux token…). Take it from `e2e next <dir>` when unsure. If the user asks "giờ làm gì?", "tiếp theo là gì?", "tôi không hiểu bước này", run `e2e next <dir>` and explain that step in 2–3 simple sentences — no commands, no jargon.

## ⛔ NON-NEGOTIABLE GATES — read before doing anything

Stop and wait for explicit user approval at every gate. Never skip, merge, or "assume approval". Record each approval with `e2e approve <dir> G<n>` ONLY after the user said yes.

| Gate | What the user approves | Nothing after this may run before approval |
|---|---|---|
| G0 | `00-ke-hoach/BRIEF.md` + `TU-LIEU.md` (idea, context, existing materials) | audience/focus questions |
| G1 | `00-ke-hoach/THIET-KE.md` (audience, focus mode, outcomes, frameworks) | outline |
| G2 | `00-ke-hoach/DAN-Y.md` + `PHAC-THAO.md` + `mindmap.json` draft | **any full chapter text** |
| G3 | 1 sample chapter, built and previewed (style, depth, tone) | writing the remaining chapters |
| G4 | Full ebook (web preview) + `prompts.json` + mindmap + glossary + teaching plan | recording kit |
| G5 | `00-ke-hoach/KICH-BAN-QUAY.md` (run-of-show for the one-take recording) | "ready to record" |
| G6 | Publish: GitHub repo name, owner/org, private/public, Pages, password | `git push`, repo creation, Pages |
| G7 | Free version selection (`free.json`) + CTA link, then its publish | building / publishing the free version |
| G8 | Video handoff: the video-to-elearning gates (PLAN → brand/test thumbnail → thumbnails → sample lesson → batch render → QA) | each v2e step — its own gates apply unchanged |
| G9 | Mux publish (policy, group, video list, MP4 on/off) and attaching videos back to the ebook | any Mux upload; rebuilding/republishing the ebook with videos |

**Hard rules**
- Do NOT write full chapter content before G2 is approved. Outline + sketch first, always. This is the single most important rule of the skill.
- Do NOT create GitHub repos, push, enable Pages, or publish anything without an explicit yes at G6/G7 for that exact action (see memory: no unrequested external actions).
- Do NOT upload to Mux, enable MP4 renditions, or change anything on Mux without the mux-publisher confirmation table + an explicit yes for THAT batch (G9). Never ask for or accept a Mux token in chat — the user enters it in the `mux-pub connect` dialog.
- The speaker's job is only: answer questions, review/adjust, record, drop the video in `quay-video/`, approve. Everything else is yours — never hand them a terminal command to run.
- Never put passwords or API keys in chat, in git, or in the ebook. Password lives in `.ebook-password` (gitignored) or env `EBOOK_PASSWORD`.
- The free version is an INTERNAL marketing decision: never mention lead funnels, "lead magnet" or the sales strategy inside learner-facing content.
- If the user explicitly says to continue past a gate unattended, you may proceed, but still self-check against the gate checklist and report what you checked.

## 0. Setup (first use)

Covered by START HERE above (`e2e start`, `e2e setup --yes`). Details:

`e2e doctor` → shows Python packages (markdown-it-py, bs4, pillow, playwright, pymupdf, pypdf, cryptography) and Chrome. Install ONLY after the user agrees (`pip install -r engine/requirements.txt`). PDF needs Chrome; web/EPUB/site do not.

`e2e new <dir> --title "…" --slug Ten-Khoa --author "GV …"` scaffolds a project: planning folder `00-ke-hoach/`, `nguon/` for raw materials, the build engine, and starter `book.json`, `mindmap.json`, `prompts.json`. Default location: next to the user's materials, named after the course.

## 1. G0 — Intake Q&A: understand what the speaker wants to teach

Goal: collect idea, context and everything that already exists, so you understand the knowledge the speaker wants to pass on. Use the question bank in [docs/HOI-DAP.md](docs/HOI-DAP.md) (Round 1).
- Ask in **2–3 short rounds**, max ~7 questions per message, grouped, each with an example answer. Offer defaults so the user can answer "ok mặc định".
- Ask for materials: past lecture recordings/transcripts, slides, mindmaps (images ok), docs (Lark/Google/Notion links), repos, case studies, student FAQs, sales page. Read every link/file you are given (built-in browser for public links). Save copies or notes in `nguon/`.
- **Brand (ask in round 1):** "Khoá thuộc đội ngũ Coachio hay cần thương hiệu riêng?" Coachio → `e2e brand-apply <dir> --coachio`, no more questions. New brand → follow [docs/THUONG-HIEU.md](docs/THUONG-HIEU.md): ask logo, colors (or extract with `e2e brand-colors`), feel, display name; write 2–3 options in `00-ke-hoach/brand-options.json`; `e2e brand-preview` → send screenshots → user picks → `e2e brand-apply --option X` → `e2e cover`. Never apply a new brand without the preview + an explicit choice. The approved brand flows to the video thumbnails via `e2e handoff`.
- Write `00-ke-hoach/TU-LIEU.md` (inventory: source → what it contains → reliability → where it will be used) and `00-ke-hoach/BRIEF.md` from `templates/BRIEF.md`.
- Mark unknowns as `❓` in the brief instead of guessing. Send a short summary + open questions. **STOP.**

## 2. G1 — Audience, focus mode, learning design

Ask Round 2 of [docs/HOI-DAP.md](docs/HOI-DAP.md). The focus mode drives everything:

| Mode | For | Writing consequences |
|---|---|---|
| `ky-thuat` (thuần kỹ thuật) | Practitioners who already know the basics | Precise terms, commands/code allowed, fewer analogies, deeper edge cases |
| `nguoi-moi` (dành cho người mới) | 100% beginners, non-tech | No terminal/commands, every term explained with an everyday analogy, glossary mandatory, copy-paste prompts for every action |
| `trung-lap` | Mixed classes | Plain language first, then a short "góc kỹ thuật" box |
| `ca-hai` (2 tầng) | Course with a free/basic layer and an advanced layer | Parts I–IV beginner, final part advanced; mark the advanced part clearly |

Then apply the frameworks in [docs/FRAMEWORKS.md](docs/FRAMEWORKS.md): Backward Design (start from outcomes) → Bloom verbs for each outcome → Action Mapping (what learners must DO, which practice proves it) → choose the lesson pattern (Gagné / Merrill) → Mayer + cognitive load for chunking. Write `00-ke-hoach/THIET-KE.md` from `templates/THIET-KE.md`. Set `book.json` → `book.mode`. **STOP.**

## 3. G2 — Outline + sketch (dàn ý + phác thảo). NO full content yet.

- `00-ke-hoach/DAN-Y.md` from `templates/DAN-Y.md`: parts → chapters → sections. Each chapter: title (verb + outcome), "Sau chương này, bạn làm được", 4–8 sections, the practice/exercise, the case or demo, prompts needed, sources from `TU-LIEU.md`, estimated video minutes.
- `00-ke-hoach/PHAC-THAO.md`: per chapter 5–10 bullet points of what will actually be said/shown (the "skeleton"), key analogy, key diagram idea, common mistakes. This is what the speaker reviews fastest.
- Draft `mindmap.json` (branches = parts/flows, leaves = concepts and steps, `chap` filled, `p` empty for now) and `book.json` parts.
- Build only the mindmap (`e2e build <dir> web`) so the user can click through it.
- Video budget check: total estimated minutes should fit the 3–4 h recording (≈180–240 min). If not, propose what to cut or move to the free/bonus layer.
- Send: outline summary table, link to the mindmap preview, open questions. **STOP.** Iterate until approved.

## 4. G3 — One sample chapter

Pick a representative chapter (usually chapter 1 or the first "how-to" chapter). Write it fully following [docs/PHONG-CACH-VIET.md](docs/PHONG-CACH-VIET.md), build, preview desktop + mobile, send screenshots + link. **STOP.** The approved sample becomes the style reference for every other chapter.

## 5. G4 — Full ebook (bản full, đầy đủ nhất)

- Write all chapters + appendices (glossary, prompt library, teaching plan, checklist/common mistakes, mindmap appendix). Long courses: write part by part; you may use parallel sub-agents per part, each given `PHONG-CACH-VIET.md`, the approved sample chapter, `DAN-Y.md`, `PHAC-THAO.md` and the relevant `nguon/` files. You own the final consistency pass.
- `prompts.json`: every prompt the learner copies, grouped by step/flow; reference the ids in `mindmap.json` leaves (`p`). The prompt appendix is generated from it (`book.prompt_appendix`).
- Case studies: real ones from the speaker's materials first; each with problem → approach → prompts → result → lessons. Never invent results or numbers; mark `❓` when unknown.
- Attribution: when content comes from another teacher, set `teacher` on that part and say so in the chapter intro.
- `e2e check <dir>` must pass (broken links, missing images, prompt ids, chapter skeleton). Build `web` (+ `epub`; `pdf` only if the user wants it now). Preview desktop + mobile with the built-in browser. Send summary + link. **STOP.**

## 6. G5 — Recording kit for the one-take video

Write `00-ke-hoach/KICH-BAN-QUAY.md` from `templates/KICH-BAN-QUAY.md` following [docs/QUAY-VIDEO.md](docs/QUAY-VIDEO.md): segments mapped to chapters with target minutes, what to open on screen, demo checklist, the "câu chuyển đoạn" (spoken transition markers that make later cutting easy), what NOT to show (logins, keys, emails), prep checklist for the day. **STOP.**

Keep segment titles identical to chapter titles and put the exact opening line in the "Câu mở đoạn" column: `v2e align` searches the transcript for it. Run `e2e handoff <dir>` at the end of G5 so `quay-video/` and its instructions exist before the recording day.

## 7. G6 — Publish the full version (ask first)

Ask in ONE message: repo name, owner (personal or org), private/public, enable GitHub Pages, password (user types it into `.ebook-password` themselves or tells you to set one), custom domain. Only after yes: `git init`/commit, create repo, enable Pages (`build_type=workflow`), push, wait for the workflow, verify the live URL (wrong password rejected, right one opens). Report link + where the password is stored.

## 8. G7 — Free version for workshops (internal)

Follow [docs/BAN-FREE.md](docs/BAN-FREE.md). Propose `free.json` (which chapters, mindmap branches, prompt steps, cases; CTA text + landing-page URL). After approval: `e2e free <dir> --config free.json --out <dir-free>` builds a separate public project (no password, CTA box after every chapter). Preview, then ask again before publishing it (G6 rules apply).

## 9. G8 — After recording: video → lessons (video-to-elearning)

Companion skills: `video-to-elearning` (CLI `v2e`, skill at `~/.claude/skills/video-to-elearning`) and `mux-publisher` (`mux-pub`). They are installed only now (lazy). If missing: ask "Tới bước video rồi — tải skill cắt video (~15 MB) nhé?" → `e2e setup --yes`; then `v2e doctor` and list each tool with its size; install only after yes. Tell them: with a Zoom .vtt transcript, Whisper (~1.6 GB) is not needed. Do not improvise a cutting pipeline.
Thumbnails use the brand approved at G0 (`handoff` carries it): Coachio → bundled kit; own brand → logo + colors pre-filled, still ONE test thumbnail to approve (v2e gate G2).

1. Before the recording day: `e2e handoff <dir>` → `00-ke-hoach/handoff-v2e.json` + folder `quay-video/` with `HUONG-DAN-DAN-VIDEO.md`. Tell the speaker in plain words where to drop the files: **Zoom Cloud → Recordings → download the MP4 (shared screen with speaker view) + "Audio transcript" (.vtt)** — the .vtt is the best input (fast, accurate). Local/OBS recordings: just the .mp4 (Whisper will transcribe).
2. When the user says the video is in: `e2e handoff <dir>` again (records the file), then `v2e init "<dir>/video-elearning" --from-ebook "<dir>"` → brief.md, glossary terms, expected lessons filled from the ebook. Follow the video-to-elearning SKILL.md from step 0/2 onward (doctor, prepare, clean-audio, transcribe).
3. `v2e align "<dir>/video-elearning"` → `work/align.md` (expected vs actual: start time per chapter from the spoken opening lines, missing chapters, chapters > 15 min to split). Use it as the backbone of PLAN.md; still read bymin.txt and verify every boundary by content. Lesson codes: `<chapter>.<n>` (7.1, 7.2…). Missing chapter → ask: skip, covered elsewhere, or record a pickup clip (`lessons[].inserts`).
4. v2e gates G1–G5 apply unchanged: PLAN approval → brand + 1 test thumbnail → thumbnail set → 1 sample lesson → batch render (may run unattended) → QA. Send approvals in ONE message where v2e allows it (thumbnails + sample).
5. After edl.json exists: `v2e align <v2e-dir> --content` → `work/lesson-content/<code>.json` from the ebook (summary, objectives, checklist, key terms, prompts, ebook link). Adjust split lessons (7.2…) to what was actually said. Quiz: not yet — when added, it will live next to lesson-content (`quiz/<code>.json`).

## 10. G9 — Mux + back into the ebook

1. Connection: `mux-pub doctor`. Not connected → follow [docs/KET-NOI-MUX.md](docs/KET-NOI-MUX.md): user creates an access token in the Mux dashboard, you run `mux-pub connect` (macOS dialog — the user pastes the token there, never in chat). Optional: Mux MCP connector (`https://mcp.mux.com`, OAuth) for browsing assets from Claude.
2. `mux-pub init <v2e-dir> --from-v2e --course "…" --group <book slug>` → manifest with titles, thumbnails, captions and the ebook-based lesson content.
3. ⛔ `mux-pub plan` → show the table, ask in ONE message: policy `signed` (paid course) or `public` (free/teaser) — NO default —, MP4 on/off, owner, exact video list. Then `upload --test --yes` (1 video, send player link) → user yes → `upload --yes` → (`mp4 --yes` only if they chose MP4) → `export`.
4. Back into the ebook: `e2e attach-video <dir> --from <v2e-dir>/mux-publish/export/<group>/course.json` → `videos.json` (public → embedded player at the top of the chapter; signed → link only if the lesson has an `lmsUrl`). Build, preview, then ask before republishing (G6 rules).
5. Report: lesson table (code · title · duration · player link), export folder, what is still missing.

## 11. Reference: project layout

```
<project>/
  00-ke-hoach/  BRIEF.md TU-LIEU.md THIET-KE.md DAN-Y.md PHAC-THAO.md KICH-BAN-QUAY.md state.json
  nguon/        raw materials from the speaker (transcripts, mindmap images, docs) — not published
  quay-video/   the speaker drops the recording here (mp4 + Zoom .vtt) — not in git
  video-elearning/  video-to-elearning project created by `v2e init --from-ebook` — not in git
  videos.json   lesson videos attached to chapters (from `e2e attach-video`)
  book.json     book info + parts (+ cover, resources, cta, mode, teacher)
  mindmap.json  interactive mindmap tree
  prompts.json  prompt library (single source for prompt.html, mindmap, prompt appendix)
  chuong-NN-*.md  phu-luc-x-*.md
  build/ build_ebook.py ebook-assets/   (engine, copied from engine/)
```
Build: `e2e build <dir> [web pdf epub site]` · Cover: `e2e cover <dir>` · Status: `e2e status <dir>`.

## 12. Lessons learned (from the Vibe Code ebook, 10/2026)

- Outline-first saved the most time; full prose before agreement on scope gets rewritten.
- Beginners: one analogy per concept (e.g. software = restaurant), tables over paragraphs, a copy-paste prompt for every action, checklist at the end of every chapter.
- One source of truth for prompts (`prompts.json`) — the ebook appendix, the prompt page and the mindmap stay in sync.
- Mindmap leaves that open a panel with explanation + prompts + "read chapter" (new tab) were the most praised feature.
- Header tabs "Mindmap" and "Bộ prompt" must be visible on every page.
- Credit each teacher per part (`teacher` field) — the user asked for this explicitly.
- Build and preview before every push; PDF can wait if the user says so.
