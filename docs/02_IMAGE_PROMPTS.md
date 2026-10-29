# Bộ prompt tạo ảnh · Mộc Viên

> **Nguồn chuẩn:** `prompts/images.json`. File này được sinh tự động bởi `scripts/render_prompt_doc.py`, nên đừng sửa tay. Muốn đổi prompt thì sửa JSON rồi chạy lại script.
> Mục tiêu: 16 ảnh trông như **một buổi chụp duy nhất**, ấm và tĩnh như ảnh tham chiếu.

## 1. Quy trình để cả bộ ảnh "một giọng"

1. **Tạo H1 trước** (ảnh neo màu). Tạo 3–4 phương án, chọn bản có: nửa trái tối, cầu thang liền mạch, ánh nắng ấm.
2. **Dùng H1 làm ảnh tham chiếu phong cách** cho mọi ảnh sau:
   - Gemini (`gemini-2.5-flash-image`): script tự đính kèm H1, chỉ lấy *màu, ánh sáng, vật liệu*, không lấy bố cục.
   - Midjourney: thêm `--sref <URL ảnh H1>` và `--style raw`.
   - ChatGPT / GPT-Image: đính kèm H1 kèm câu "match the colour grade, light and material palette of the attached image; do not copy its composition".
3. **Khoá series:** V1–V4 dùng chung `VILLA_SERIES` (cùng góc máy, cùng giờ, cùng bầu trời); G1–G6 dùng chung `ROOM_SERIES`. Tạo các ảnh trong cùng một series liên tiếp nhau.
4. **Grade chung:** `process_images.py` áp cùng một mức lift blacks / saturation / warmth (chỉnh trong `project.config.json → images.grade`).
5. **Kiểm tra:** đặt 16 ảnh cạnh nhau. Ảnh nào "lạc tông" thì tạo lại với `--only ID --force`.

## 2. Cấu trúc một prompt

```
[Nội dung cảnh]  →  COMPOSITION — [bố cục, chỗ chừa cho chữ]  →  [block: HANDS / TEXT_SPACE / BLEND_CREAM]
→  [SERIES LOCK nếu có]  →  STYLE DNA  →  Avoid: [negative]
```

Script ghép tự động theo đúng thứ tự trên. Phần **Prompt cuối cùng** ở mỗi ảnh bên dưới là bản đã ghép, dán thẳng vào công cụ tạo ảnh là dùng được.

## 3. Các khối dùng chung

### STYLE DNA (ghép vào mọi ảnh)
```text
STYLE DNA — warm luxury architectural and interior photography for a high-end residential brand, editorial and quiet, like a spread in a premium design magazine. Palette: espresso brown (#2A1F17), warm walnut, honey-toned solid white oak, travertine and limewash cream (#F3EBE2), caramel accents (#CFAE86), thin matte-black metal, a little brushed bronze; greens only from real foliage (olive trees, pines), always muted. Light: low golden sun raking through tall glass, warm 2700K concealed LED lines under stair treads and in ceiling coves, soft bounce light; deep but transparent shadows, creamy rolled-off highlights, gentle natural vignette. Forms and materials: sculptural curves (spiral stairs, arched openings, rounded plaster walls), solid oak and walnut joinery, travertine floors, bouclé and linen upholstery in oatmeal and ivory, an olive tree in a large matte planter, very few objects. Camera: full-frame architectural photography, 24–35 mm for interiors, verticals perfectly corrected, eye level around 1.4 m, f/5.6 with soft depth falloff, fine natural film grain, photorealistic. Grade: warm, low saturation, slightly lifted blacks, brown-gold midtones, cohesive across the whole set.
```

### NEGATIVE (ghép vào mọi ảnh)
```text
cold or blue cast, neon, glossy CGI render look, plastic surfaces, oversaturation, HDR halos, harsh flash, clutter, visible logos or brand names, any text or lettering, watermark, signature, distorted or bent vertical lines, warped perspective, extra or merged stair treads, impossible geometry, floating furniture, duplicated objects, people (unless requested), malformed hands or fingers.
```

### Block `HANDS`
```text
HANDS — a Vietnamese artisan's hands: fair, smooth and even skin tone, clean short natural nails, realistic anatomy with exactly five fingers on each hand, relaxed natural pose, fine skin texture visible but not rough; no face in frame; dark charcoal linen work shirt with rolled sleeves.
```

### Block `TEXT_SPACE_LEFT`
```text
TEXT SPACE — the left 42% of the frame must stay calm and dark (luminance under 20%), low detail, no bright highlights or windows there; it will hold a large headline.
```

### Block `TEXT_SPACE_TOP`
```text
TEXT SPACE — the upper 45% of the frame must stay calm and dark, low detail; it will hold a large headline.
```

### Block `BLEND_CREAM`
```text
BACKGROUND — the background is a flat, evenly lit warm cream limewash wall (#F2EBE4) with no texture variation near the edges, so the photo can melt seamlessly into a cream web card; generous empty space on both sides.
```

### Series `VILLA_SERIES`
```text
SERIES LOCK (identical across V1–V4) — same photographic setup for every image: camera 1.6 m high in the front garden, 35 mm, three-quarter front view, villa occupying the central 70% of the frame, golden hour sun from the left at 15° elevation, the same soft peach-to-dusty-rose sky, the same pine forest backdrop, warm light glowing from inside every window, a strip of manicured lawn and low ornamental grasses in the foreground. Architecture language shared by all: low horizontal massing, warm limewash and travertine walls, deep eaves clad in oak slats, large arched openings, bronze-framed glazing, flat roofs with thin edges.
```

### Series `ROOM_SERIES`
```text
SERIES LOCK (identical across G1–G6) — same house, same materials, same late-afternoon golden light from tall west-facing glass, camera at 1.4 m, 28 mm, verticals corrected, vertical 4:5 composition with the main subject in the middle third and calm floor in the lower fifth (a caption sits below the image), no people.
```

## 4. Danh sách ảnh

| ID | File web | Section | Tỉ lệ | Xuất (px) | Ảnh sản phẩm |
|---|---|---|---|---|---|
| **H1** | `hero.webp` | S1 Hero | 16:9 | 2400×1350 | — |
| **H1M** | `hero-m.webp` | S1 Hero (mobile) | 4:5 | 1200×1500 | — |
| **S2** | `story-hands.webp` | S2 Câu chuyện | 4:3 | 1600×1200 | — |
| **G0** | `spaces-arch.webp` | S3 Không gian (mở màn vòm) | 16:9 | 2400×1350 | có — dự án thật phải dùng ảnh chính thức |
| **G1** | `room-1.webp` | S3 Không gian | 4:5 | 1200×1500 | — |
| **G2** | `room-2.webp` | S3 Không gian | 4:5 | 1200×1500 | — |
| **G3** | `room-3.webp` | S3 Không gian | 4:5 | 1200×1500 | — |
| **G4** | `room-4.webp` | S3 Không gian | 4:5 | 1200×1500 | — |
| **G5** | `room-5.webp` | S3 Không gian | 4:5 | 1200×1500 | — |
| **G6** | `room-6.webp` | S3 Không gian | 4:5 | 1200×1500 | — |
| **V1** | `villa-1.webp` | S4 Dòng biệt thự | 4:3 | 1200×900 | có — dự án thật phải dùng ảnh chính thức |
| **V2** | `villa-2.webp` | S4 Dòng biệt thự | 4:3 | 1200×900 | có — dự án thật phải dùng ảnh chính thức |
| **V3** | `villa-3.webp` | S4 Dòng biệt thự | 4:3 | 1200×900 | có — dự án thật phải dùng ảnh chính thức |
| **V4** | `villa-4.webp` | S4 Dòng biệt thự | 4:3 | 1200×900 | có — dự án thật phải dùng ảnh chính thức |
| **B1** | `banner-plans.webp` | S4 Banner hoàn thiện riêng | 21:9 | 2400×1030 | — |
| **F1** | `invite-vase.webp` | S5 Lời mời | 16:9 | 1800×1012 | — |

## 5. Prompt từng ảnh

### H1 · S1 Hero · ảnh neo màu
- Lưu ảnh gốc: `assets/raw/H1.png` · Tỉ lệ **16:9**
- Block: `TEXT_SPACE_LEFT`
- Kiểm tra sau khi tạo: Bậc thang liền mạch, không bậc thừa/biến dạng · Nửa trái đủ tối để chữ trắng đọc rõ · Không có chữ/logo · Ánh sáng ấm, không ám xanh

**Cảnh:** Interior of a double-height villa foyer at golden hour. In the right 55% of the frame, a sculptural floating spiral staircase in solid honey-toned oak sweeps up in a wide elegant curve to an upper gallery; every tread is lit from beneath by a warm LED line, and a smooth continuous oak handrail follows the curve. Behind the stairs, floor-to-ceiling glass reveals a pine forest and a sliver of lake glowing in late sun; long beams of sunlight rake across a honed travertine floor. A mature olive tree in a large matte black planter stands at the foot of the stairs. The left part of the room falls into deep, warm shadow: a walnut-panelled wall and a low bouclé sofa almost in silhouette.

**Bố cục:** Wide 16:9, eye level, slight one-point perspective toward the windows; staircase and brightest light confined to the right 55%; foreground floor calm; nothing bright in the left 42%.

<details><summary>Prompt cuối cùng (đã ghép)</summary>

```text
Interior of a double-height villa foyer at golden hour. In the right 55% of the frame, a sculptural floating spiral staircase in solid honey-toned oak sweeps up in a wide elegant curve to an upper gallery; every tread is lit from beneath by a warm LED line, and a smooth continuous oak handrail follows the curve. Behind the stairs, floor-to-ceiling glass reveals a pine forest and a sliver of lake glowing in late sun; long beams of sunlight rake across a honed travertine floor. A mature olive tree in a large matte black planter stands at the foot of the stairs. The left part of the room falls into deep, warm shadow: a walnut-panelled wall and a low bouclé sofa almost in silhouette.

COMPOSITION — Wide 16:9, eye level, slight one-point perspective toward the windows; staircase and brightest light confined to the right 55%; foreground floor calm; nothing bright in the left 42%.

TEXT SPACE — the left 42% of the frame must stay calm and dark (luminance under 20%), low detail, no bright highlights or windows there; it will hold a large headline.

STYLE DNA — warm luxury architectural and interior photography for a high-end residential brand, editorial and quiet, like a spread in a premium design magazine. Palette: espresso brown (#2A1F17), warm walnut, honey-toned solid white oak, travertine and limewash cream (#F3EBE2), caramel accents (#CFAE86), thin matte-black metal, a little brushed bronze; greens only from real foliage (olive trees, pines), always muted. Light: low golden sun raking through tall glass, warm 2700K concealed LED lines under stair treads and in ceiling coves, soft bounce light; deep but transparent shadows, creamy rolled-off highlights, gentle natural vignette. Forms and materials: sculptural curves (spiral stairs, arched openings, rounded plaster walls), solid oak and walnut joinery, travertine floors, bouclé and linen upholstery in oatmeal and ivory, an olive tree in a large matte planter, very few objects. Camera: full-frame architectural photography, 24–35 mm for interiors, verticals perfectly corrected, eye level around 1.4 m, f/5.6 with soft depth falloff, fine natural film grain, photorealistic. Grade: warm, low saturation, slightly lifted blacks, brown-gold midtones, cohesive across the whole set.

Avoid: cold or blue cast, neon, glossy CGI render look, plastic surfaces, oversaturation, HDR halos, harsh flash, clutter, visible logos or brand names, any text or lettering, watermark, signature, distorted or bent vertical lines, warped perspective, extra or merged stair treads, impossible geometry, floating furniture, duplicated objects, people (unless requested), malformed hands or fingers.
```
</details>

### H1M · S1 Hero (mobile)
- Lưu ảnh gốc: `assets/raw/H1M.png` · Tỉ lệ **4:5**
- Block: `TEXT_SPACE_TOP`
- Kiểm tra sau khi tạo: Cùng chất liệu/ánh sáng với H1 · 45% phía trên tối và trống

**Cảnh:** The same double-height villa foyer at golden hour, framed vertically: the solid oak floating spiral staircase with warm LED-lit treads rises through the lower half of the frame, the olive tree in a matte black planter at its foot, travertine floor with long sun beams; above, the ceiling and upper walls fall into deep warm shadow.

**Bố cục:** Vertical 4:5, staircase in the lower 55%, centred slightly right; upper 45% dark and calm.

<details><summary>Prompt cuối cùng (đã ghép)</summary>

```text
The same double-height villa foyer at golden hour, framed vertically: the solid oak floating spiral staircase with warm LED-lit treads rises through the lower half of the frame, the olive tree in a matte black planter at its foot, travertine floor with long sun beams; above, the ceiling and upper walls fall into deep warm shadow.

COMPOSITION — Vertical 4:5, staircase in the lower 55%, centred slightly right; upper 45% dark and calm.

TEXT SPACE — the upper 45% of the frame must stay calm and dark, low detail; it will hold a large headline.

STYLE DNA — warm luxury architectural and interior photography for a high-end residential brand, editorial and quiet, like a spread in a premium design magazine. Palette: espresso brown (#2A1F17), warm walnut, honey-toned solid white oak, travertine and limewash cream (#F3EBE2), caramel accents (#CFAE86), thin matte-black metal, a little brushed bronze; greens only from real foliage (olive trees, pines), always muted. Light: low golden sun raking through tall glass, warm 2700K concealed LED lines under stair treads and in ceiling coves, soft bounce light; deep but transparent shadows, creamy rolled-off highlights, gentle natural vignette. Forms and materials: sculptural curves (spiral stairs, arched openings, rounded plaster walls), solid oak and walnut joinery, travertine floors, bouclé and linen upholstery in oatmeal and ivory, an olive tree in a large matte planter, very few objects. Camera: full-frame architectural photography, 24–35 mm for interiors, verticals perfectly corrected, eye level around 1.4 m, f/5.6 with soft depth falloff, fine natural film grain, photorealistic. Grade: warm, low saturation, slightly lifted blacks, brown-gold midtones, cohesive across the whole set.

Avoid: cold or blue cast, neon, glossy CGI render look, plastic surfaces, oversaturation, HDR halos, harsh flash, clutter, visible logos or brand names, any text or lettering, watermark, signature, distorted or bent vertical lines, warped perspective, extra or merged stair treads, impossible geometry, floating furniture, duplicated objects, people (unless requested), malformed hands or fingers.
```
</details>

### S2 · S2 Câu chuyện
- Lưu ảnh gốc: `assets/raw/S2.png` · Tỉ lệ **4:3**
- Block: `HANDS`
- Kiểm tra sau khi tạo: Đúng 5 ngón mỗi bàn tay, khớp ngón tự nhiên · Da sáng, đều màu · Không lộ mặt · Đường cong gỗ mượt, vân gỗ thật

**Cảnh:** Close-up of an artisan's two hands sanding the smooth curved edge of a solid white-oak handrail section clamped on a workbench. The sweeping curve of wood fills the lower right of the frame, its grain glowing honey-gold; one hand rests flat on the curve, the other holds a small sanding block. Fine wood dust and a few pale shavings on the bench. Warm window light from the left, the workshop background falling away into deep brown darkness.

**Bố cục:** 4:3, 50 mm, f/2.8, slightly high angle; hands in the upper-left to centre, the curved wood dominating the right half; dark background on the right edge.

<details><summary>Prompt cuối cùng (đã ghép)</summary>

```text
Close-up of an artisan's two hands sanding the smooth curved edge of a solid white-oak handrail section clamped on a workbench. The sweeping curve of wood fills the lower right of the frame, its grain glowing honey-gold; one hand rests flat on the curve, the other holds a small sanding block. Fine wood dust and a few pale shavings on the bench. Warm window light from the left, the workshop background falling away into deep brown darkness.

COMPOSITION — 4:3, 50 mm, f/2.8, slightly high angle; hands in the upper-left to centre, the curved wood dominating the right half; dark background on the right edge.

HANDS — a Vietnamese artisan's hands: fair, smooth and even skin tone, clean short natural nails, realistic anatomy with exactly five fingers on each hand, relaxed natural pose, fine skin texture visible but not rough; no face in frame; dark charcoal linen work shirt with rolled sleeves.

STYLE DNA — warm luxury architectural and interior photography for a high-end residential brand, editorial and quiet, like a spread in a premium design magazine. Palette: espresso brown (#2A1F17), warm walnut, honey-toned solid white oak, travertine and limewash cream (#F3EBE2), caramel accents (#CFAE86), thin matte-black metal, a little brushed bronze; greens only from real foliage (olive trees, pines), always muted. Light: low golden sun raking through tall glass, warm 2700K concealed LED lines under stair treads and in ceiling coves, soft bounce light; deep but transparent shadows, creamy rolled-off highlights, gentle natural vignette. Forms and materials: sculptural curves (spiral stairs, arched openings, rounded plaster walls), solid oak and walnut joinery, travertine floors, bouclé and linen upholstery in oatmeal and ivory, an olive tree in a large matte planter, very few objects. Camera: full-frame architectural photography, 24–35 mm for interiors, verticals perfectly corrected, eye level around 1.4 m, f/5.6 with soft depth falloff, fine natural film grain, photorealistic. Grade: warm, low saturation, slightly lifted blacks, brown-gold midtones, cohesive across the whole set.

Avoid: cold or blue cast, neon, glossy CGI render look, plastic surfaces, oversaturation, HDR halos, harsh flash, clutter, visible logos or brand names, any text or lettering, watermark, signature, distorted or bent vertical lines, warped perspective, extra or merged stair treads, impossible geometry, floating furniture, duplicated objects, people (unless requested), malformed hands or fingers.
```
</details>

### G0 · S3 Không gian (mở màn vòm)
- Lưu ảnh gốc: `assets/raw/G0.png` · Tỉ lệ **16:9**
- Kiểm tra sau khi tạo: Bố cục đối xứng, chủ thể nằm trong 40% giữa · Mặt nước phản chiếu sạch · Kiến trúc cùng ngôn ngữ với V1–V4

**Cảnh:** Exterior of a contemporary low-rise villa on a gentle pine-covered hillside above a perfectly still lake at golden hour. Warm limewash and travertine walls, deep eaves clad in oak slats, a row of tall arched openings on the ground floor glowing with warm interior light, a long reflecting pool in front mirroring the arches, slender pines framing both sides. Sky a soft gradient from peach near the horizon to dusty rose above.

**Bố cục:** 16:9, symmetrical, camera at 1.5 m across the reflecting pool; the villa and its arches confined to the central 40% of the width (the image is first shown through a narrow arch-shaped window, then expands to full screen); calm water in the lower third.

<details><summary>Prompt cuối cùng (đã ghép)</summary>

```text
Exterior of a contemporary low-rise villa on a gentle pine-covered hillside above a perfectly still lake at golden hour. Warm limewash and travertine walls, deep eaves clad in oak slats, a row of tall arched openings on the ground floor glowing with warm interior light, a long reflecting pool in front mirroring the arches, slender pines framing both sides. Sky a soft gradient from peach near the horizon to dusty rose above.

COMPOSITION — 16:9, symmetrical, camera at 1.5 m across the reflecting pool; the villa and its arches confined to the central 40% of the width (the image is first shown through a narrow arch-shaped window, then expands to full screen); calm water in the lower third.

STYLE DNA — warm luxury architectural and interior photography for a high-end residential brand, editorial and quiet, like a spread in a premium design magazine. Palette: espresso brown (#2A1F17), warm walnut, honey-toned solid white oak, travertine and limewash cream (#F3EBE2), caramel accents (#CFAE86), thin matte-black metal, a little brushed bronze; greens only from real foliage (olive trees, pines), always muted. Light: low golden sun raking through tall glass, warm 2700K concealed LED lines under stair treads and in ceiling coves, soft bounce light; deep but transparent shadows, creamy rolled-off highlights, gentle natural vignette. Forms and materials: sculptural curves (spiral stairs, arched openings, rounded plaster walls), solid oak and walnut joinery, travertine floors, bouclé and linen upholstery in oatmeal and ivory, an olive tree in a large matte planter, very few objects. Camera: full-frame architectural photography, 24–35 mm for interiors, verticals perfectly corrected, eye level around 1.4 m, f/5.6 with soft depth falloff, fine natural film grain, photorealistic. Grade: warm, low saturation, slightly lifted blacks, brown-gold midtones, cohesive across the whole set.

Avoid: cold or blue cast, neon, glossy CGI render look, plastic surfaces, oversaturation, HDR halos, harsh flash, clutter, visible logos or brand names, any text or lettering, watermark, signature, distorted or bent vertical lines, warped perspective, extra or merged stair treads, impossible geometry, floating furniture, duplicated objects, people (unless requested), malformed hands or fingers.
```
</details>

### G1 · S3 Không gian
- Lưu ảnh gốc: `assets/raw/G1.png` · Tỉ lệ **4:5**
- Series: `ROOM_SERIES`
- Kiểm tra sau khi tạo: Cầu thang khớp với H1 · Không người

**Cảnh:** A double-height living room with a curved limewash wall, a low modular sofa in oatmeal bouclé, a travertine coffee table carved as one block, and the solid oak spiral staircase rising at the edge of the frame; tall glass behind opens to pines with long golden light across the floor.

**Bố cục:** Sofa and staircase in the middle third, ceiling height emphasised.

<details><summary>Prompt cuối cùng (đã ghép)</summary>

```text
A double-height living room with a curved limewash wall, a low modular sofa in oatmeal bouclé, a travertine coffee table carved as one block, and the solid oak spiral staircase rising at the edge of the frame; tall glass behind opens to pines with long golden light across the floor.

COMPOSITION — Sofa and staircase in the middle third, ceiling height emphasised.

SERIES LOCK (identical across G1–G6) — same house, same materials, same late-afternoon golden light from tall west-facing glass, camera at 1.4 m, 28 mm, verticals corrected, vertical 4:5 composition with the main subject in the middle third and calm floor in the lower fifth (a caption sits below the image), no people.

STYLE DNA — warm luxury architectural and interior photography for a high-end residential brand, editorial and quiet, like a spread in a premium design magazine. Palette: espresso brown (#2A1F17), warm walnut, honey-toned solid white oak, travertine and limewash cream (#F3EBE2), caramel accents (#CFAE86), thin matte-black metal, a little brushed bronze; greens only from real foliage (olive trees, pines), always muted. Light: low golden sun raking through tall glass, warm 2700K concealed LED lines under stair treads and in ceiling coves, soft bounce light; deep but transparent shadows, creamy rolled-off highlights, gentle natural vignette. Forms and materials: sculptural curves (spiral stairs, arched openings, rounded plaster walls), solid oak and walnut joinery, travertine floors, bouclé and linen upholstery in oatmeal and ivory, an olive tree in a large matte planter, very few objects. Camera: full-frame architectural photography, 24–35 mm for interiors, verticals perfectly corrected, eye level around 1.4 m, f/5.6 with soft depth falloff, fine natural film grain, photorealistic. Grade: warm, low saturation, slightly lifted blacks, brown-gold midtones, cohesive across the whole set.

Avoid: cold or blue cast, neon, glossy CGI render look, plastic surfaces, oversaturation, HDR halos, harsh flash, clutter, visible logos or brand names, any text or lettering, watermark, signature, distorted or bent vertical lines, warped perspective, extra or merged stair treads, impossible geometry, floating furniture, duplicated objects, people (unless requested), malformed hands or fingers.
```
</details>

### G2 · S3 Không gian
- Lưu ảnh gốc: `assets/raw/G2.png` · Tỉ lệ **4:5**
- Series: `ROOM_SERIES`
- Kiểm tra sau khi tạo: Đá travertine có lỗ rỗ tự nhiên · Không vật dụng thừa

**Cảnh:** An open kitchen with a monolithic honed travertine island, flat-front walnut cabinetry to the ceiling, a slim brushed-bronze tap, three hand-blown amber glass pendants, a ceramic bowl of figs on the island, late sun striping across the stone through a tall window.

**Bố cục:** Island centred in the middle third, pendants in the upper third.

<details><summary>Prompt cuối cùng (đã ghép)</summary>

```text
An open kitchen with a monolithic honed travertine island, flat-front walnut cabinetry to the ceiling, a slim brushed-bronze tap, three hand-blown amber glass pendants, a ceramic bowl of figs on the island, late sun striping across the stone through a tall window.

COMPOSITION — Island centred in the middle third, pendants in the upper third.

SERIES LOCK (identical across G1–G6) — same house, same materials, same late-afternoon golden light from tall west-facing glass, camera at 1.4 m, 28 mm, verticals corrected, vertical 4:5 composition with the main subject in the middle third and calm floor in the lower fifth (a caption sits below the image), no people.

STYLE DNA — warm luxury architectural and interior photography for a high-end residential brand, editorial and quiet, like a spread in a premium design magazine. Palette: espresso brown (#2A1F17), warm walnut, honey-toned solid white oak, travertine and limewash cream (#F3EBE2), caramel accents (#CFAE86), thin matte-black metal, a little brushed bronze; greens only from real foliage (olive trees, pines), always muted. Light: low golden sun raking through tall glass, warm 2700K concealed LED lines under stair treads and in ceiling coves, soft bounce light; deep but transparent shadows, creamy rolled-off highlights, gentle natural vignette. Forms and materials: sculptural curves (spiral stairs, arched openings, rounded plaster walls), solid oak and walnut joinery, travertine floors, bouclé and linen upholstery in oatmeal and ivory, an olive tree in a large matte planter, very few objects. Camera: full-frame architectural photography, 24–35 mm for interiors, verticals perfectly corrected, eye level around 1.4 m, f/5.6 with soft depth falloff, fine natural film grain, photorealistic. Grade: warm, low saturation, slightly lifted blacks, brown-gold midtones, cohesive across the whole set.

Avoid: cold or blue cast, neon, glossy CGI render look, plastic surfaces, oversaturation, HDR halos, harsh flash, clutter, visible logos or brand names, any text or lettering, watermark, signature, distorted or bent vertical lines, warped perspective, extra or merged stair treads, impossible geometry, floating furniture, duplicated objects, people (unless requested), malformed hands or fingers.
```
</details>

### G3 · S3 Không gian
- Lưu ảnh gốc: `assets/raw/G3.png` · Tỉ lệ **4:5**
- Series: `ROOM_SERIES`
- Kiểm tra sau khi tạo: Gáy sách không có chữ đọc được · Ánh sáng ấm, mềm

**Cảnh:** A private library with floor-to-ceiling walnut shelving softly backlit by concealed warm LED, a rolling bronze ladder, a deep cognac leather lounge chair with ottoman, a round travertine side table with a reading lamp, and a narrow arched window showing pines in evening light.

**Bố cục:** Lounge chair in the middle third, shelving filling the background.

<details><summary>Prompt cuối cùng (đã ghép)</summary>

```text
A private library with floor-to-ceiling walnut shelving softly backlit by concealed warm LED, a rolling bronze ladder, a deep cognac leather lounge chair with ottoman, a round travertine side table with a reading lamp, and a narrow arched window showing pines in evening light.

COMPOSITION — Lounge chair in the middle third, shelving filling the background.

SERIES LOCK (identical across G1–G6) — same house, same materials, same late-afternoon golden light from tall west-facing glass, camera at 1.4 m, 28 mm, verticals corrected, vertical 4:5 composition with the main subject in the middle third and calm floor in the lower fifth (a caption sits below the image), no people.

STYLE DNA — warm luxury architectural and interior photography for a high-end residential brand, editorial and quiet, like a spread in a premium design magazine. Palette: espresso brown (#2A1F17), warm walnut, honey-toned solid white oak, travertine and limewash cream (#F3EBE2), caramel accents (#CFAE86), thin matte-black metal, a little brushed bronze; greens only from real foliage (olive trees, pines), always muted. Light: low golden sun raking through tall glass, warm 2700K concealed LED lines under stair treads and in ceiling coves, soft bounce light; deep but transparent shadows, creamy rolled-off highlights, gentle natural vignette. Forms and materials: sculptural curves (spiral stairs, arched openings, rounded plaster walls), solid oak and walnut joinery, travertine floors, bouclé and linen upholstery in oatmeal and ivory, an olive tree in a large matte planter, very few objects. Camera: full-frame architectural photography, 24–35 mm for interiors, verticals perfectly corrected, eye level around 1.4 m, f/5.6 with soft depth falloff, fine natural film grain, photorealistic. Grade: warm, low saturation, slightly lifted blacks, brown-gold midtones, cohesive across the whole set.

Avoid: cold or blue cast, neon, glossy CGI render look, plastic surfaces, oversaturation, HDR halos, harsh flash, clutter, visible logos or brand names, any text or lettering, watermark, signature, distorted or bent vertical lines, warped perspective, extra or merged stair treads, impossible geometry, floating furniture, duplicated objects, people (unless requested), malformed hands or fingers.
```
</details>

### G4 · S3 Không gian
- Lưu ảnh gốc: `assets/raw/G4.png` · Tỉ lệ **4:5**
- Series: `ROOM_SERIES`
- Kiểm tra sau khi tạo: Ga gối nhăn tự nhiên · Mặt hồ phẳng, có sương nhẹ

**Cảnh:** A master bedroom with a low white-oak platform bed dressed in ivory and oatmeal linen, a curved upholstered headboard, sheer linen curtains lifting slightly, and floor-to-ceiling glass opening onto a calm lake veiled in thin evening mist with pines on the far shore.

**Bố cục:** Bed in the lower-middle third, window and lake view behind.

<details><summary>Prompt cuối cùng (đã ghép)</summary>

```text
A master bedroom with a low white-oak platform bed dressed in ivory and oatmeal linen, a curved upholstered headboard, sheer linen curtains lifting slightly, and floor-to-ceiling glass opening onto a calm lake veiled in thin evening mist with pines on the far shore.

COMPOSITION — Bed in the lower-middle third, window and lake view behind.

SERIES LOCK (identical across G1–G6) — same house, same materials, same late-afternoon golden light from tall west-facing glass, camera at 1.4 m, 28 mm, verticals corrected, vertical 4:5 composition with the main subject in the middle third and calm floor in the lower fifth (a caption sits below the image), no people.

STYLE DNA — warm luxury architectural and interior photography for a high-end residential brand, editorial and quiet, like a spread in a premium design magazine. Palette: espresso brown (#2A1F17), warm walnut, honey-toned solid white oak, travertine and limewash cream (#F3EBE2), caramel accents (#CFAE86), thin matte-black metal, a little brushed bronze; greens only from real foliage (olive trees, pines), always muted. Light: low golden sun raking through tall glass, warm 2700K concealed LED lines under stair treads and in ceiling coves, soft bounce light; deep but transparent shadows, creamy rolled-off highlights, gentle natural vignette. Forms and materials: sculptural curves (spiral stairs, arched openings, rounded plaster walls), solid oak and walnut joinery, travertine floors, bouclé and linen upholstery in oatmeal and ivory, an olive tree in a large matte planter, very few objects. Camera: full-frame architectural photography, 24–35 mm for interiors, verticals perfectly corrected, eye level around 1.4 m, f/5.6 with soft depth falloff, fine natural film grain, photorealistic. Grade: warm, low saturation, slightly lifted blacks, brown-gold midtones, cohesive across the whole set.

Avoid: cold or blue cast, neon, glossy CGI render look, plastic surfaces, oversaturation, HDR halos, harsh flash, clutter, visible logos or brand names, any text or lettering, watermark, signature, distorted or bent vertical lines, warped perspective, extra or merged stair treads, impossible geometry, floating furniture, duplicated objects, people (unless requested), malformed hands or fingers.
```
</details>

### G5 · S3 Không gian
- Lưu ảnh gốc: `assets/raw/G5.png` · Tỉ lệ **4:5**
- Series: `ROOM_SERIES`
- Kiểm tra sau khi tạo: Bồn tắm liền khối, không méo · Vòi đồng đúng tỉ lệ

**Cảnh:** A spa bathroom carved in travertine: a freestanding oval bathtub cut from a single block of travertine, a wall-mounted brushed-bronze spout, a fluted oak bench with folded linen towels, a single dried olive branch in a stoneware vase, warm light grazing the stone from a high slot window.

**Bố cục:** Bathtub centred in the middle third, slot window high in the frame.

<details><summary>Prompt cuối cùng (đã ghép)</summary>

```text
A spa bathroom carved in travertine: a freestanding oval bathtub cut from a single block of travertine, a wall-mounted brushed-bronze spout, a fluted oak bench with folded linen towels, a single dried olive branch in a stoneware vase, warm light grazing the stone from a high slot window.

COMPOSITION — Bathtub centred in the middle third, slot window high in the frame.

SERIES LOCK (identical across G1–G6) — same house, same materials, same late-afternoon golden light from tall west-facing glass, camera at 1.4 m, 28 mm, verticals corrected, vertical 4:5 composition with the main subject in the middle third and calm floor in the lower fifth (a caption sits below the image), no people.

STYLE DNA — warm luxury architectural and interior photography for a high-end residential brand, editorial and quiet, like a spread in a premium design magazine. Palette: espresso brown (#2A1F17), warm walnut, honey-toned solid white oak, travertine and limewash cream (#F3EBE2), caramel accents (#CFAE86), thin matte-black metal, a little brushed bronze; greens only from real foliage (olive trees, pines), always muted. Light: low golden sun raking through tall glass, warm 2700K concealed LED lines under stair treads and in ceiling coves, soft bounce light; deep but transparent shadows, creamy rolled-off highlights, gentle natural vignette. Forms and materials: sculptural curves (spiral stairs, arched openings, rounded plaster walls), solid oak and walnut joinery, travertine floors, bouclé and linen upholstery in oatmeal and ivory, an olive tree in a large matte planter, very few objects. Camera: full-frame architectural photography, 24–35 mm for interiors, verticals perfectly corrected, eye level around 1.4 m, f/5.6 with soft depth falloff, fine natural film grain, photorealistic. Grade: warm, low saturation, slightly lifted blacks, brown-gold midtones, cohesive across the whole set.

Avoid: cold or blue cast, neon, glossy CGI render look, plastic surfaces, oversaturation, HDR halos, harsh flash, clutter, visible logos or brand names, any text or lettering, watermark, signature, distorted or bent vertical lines, warped perspective, extra or merged stair treads, impossible geometry, floating furniture, duplicated objects, people (unless requested), malformed hands or fingers.
```
</details>

### G6 · S3 Không gian
- Lưu ảnh gốc: `assets/raw/G6.png` · Tỉ lệ **4:5**
- Series: `ROOM_SERIES`
- Kiểm tra sau khi tạo: Đường tràn bờ thẳng · Hai mặt nước liền mạch · Không người

**Cảnh:** An outdoor teak terrace with a long infinity-edge pool whose edge visually merges with the lake below, two low teak loungers with sand linen cushions, a pine branch framing the top of the image, the sun just above the far hills casting a warm golden path across both waters.

**Bố cục:** Pool edge on a horizontal line at about 55% height; loungers in the lower third.

<details><summary>Prompt cuối cùng (đã ghép)</summary>

```text
An outdoor teak terrace with a long infinity-edge pool whose edge visually merges with the lake below, two low teak loungers with sand linen cushions, a pine branch framing the top of the image, the sun just above the far hills casting a warm golden path across both waters.

COMPOSITION — Pool edge on a horizontal line at about 55% height; loungers in the lower third.

SERIES LOCK (identical across G1–G6) — same house, same materials, same late-afternoon golden light from tall west-facing glass, camera at 1.4 m, 28 mm, verticals corrected, vertical 4:5 composition with the main subject in the middle third and calm floor in the lower fifth (a caption sits below the image), no people.

STYLE DNA — warm luxury architectural and interior photography for a high-end residential brand, editorial and quiet, like a spread in a premium design magazine. Palette: espresso brown (#2A1F17), warm walnut, honey-toned solid white oak, travertine and limewash cream (#F3EBE2), caramel accents (#CFAE86), thin matte-black metal, a little brushed bronze; greens only from real foliage (olive trees, pines), always muted. Light: low golden sun raking through tall glass, warm 2700K concealed LED lines under stair treads and in ceiling coves, soft bounce light; deep but transparent shadows, creamy rolled-off highlights, gentle natural vignette. Forms and materials: sculptural curves (spiral stairs, arched openings, rounded plaster walls), solid oak and walnut joinery, travertine floors, bouclé and linen upholstery in oatmeal and ivory, an olive tree in a large matte planter, very few objects. Camera: full-frame architectural photography, 24–35 mm for interiors, verticals perfectly corrected, eye level around 1.4 m, f/5.6 with soft depth falloff, fine natural film grain, photorealistic. Grade: warm, low saturation, slightly lifted blacks, brown-gold midtones, cohesive across the whole set.

Avoid: cold or blue cast, neon, glossy CGI render look, plastic surfaces, oversaturation, HDR halos, harsh flash, clutter, visible logos or brand names, any text or lettering, watermark, signature, distorted or bent vertical lines, warped perspective, extra or merged stair treads, impossible geometry, floating furniture, duplicated objects, people (unless requested), malformed hands or fingers.
```
</details>

### V1 · S4 Dòng biệt thự
- Lưu ảnh gốc: `assets/raw/V1.png` · Tỉ lệ **4:3**
- Series: `VILLA_SERIES`
- Kiểm tra sau khi tạo: Cùng bầu trời/góc máy với V2–V4

**Cảnh:** Villa type 'Ven Hồ': a one-to-two-storey lakefront detached villa stretching horizontally along the water, a wide oak deck stepping down to a private timber jetty, arched glazed doors open to the deck.

**Bố cục:** Lake visible on the right edge.

<details><summary>Prompt cuối cùng (đã ghép)</summary>

```text
Villa type 'Ven Hồ': a one-to-two-storey lakefront detached villa stretching horizontally along the water, a wide oak deck stepping down to a private timber jetty, arched glazed doors open to the deck.

COMPOSITION — Lake visible on the right edge.

SERIES LOCK (identical across V1–V4) — same photographic setup for every image: camera 1.6 m high in the front garden, 35 mm, three-quarter front view, villa occupying the central 70% of the frame, golden hour sun from the left at 15° elevation, the same soft peach-to-dusty-rose sky, the same pine forest backdrop, warm light glowing from inside every window, a strip of manicured lawn and low ornamental grasses in the foreground. Architecture language shared by all: low horizontal massing, warm limewash and travertine walls, deep eaves clad in oak slats, large arched openings, bronze-framed glazing, flat roofs with thin edges.

STYLE DNA — warm luxury architectural and interior photography for a high-end residential brand, editorial and quiet, like a spread in a premium design magazine. Palette: espresso brown (#2A1F17), warm walnut, honey-toned solid white oak, travertine and limewash cream (#F3EBE2), caramel accents (#CFAE86), thin matte-black metal, a little brushed bronze; greens only from real foliage (olive trees, pines), always muted. Light: low golden sun raking through tall glass, warm 2700K concealed LED lines under stair treads and in ceiling coves, soft bounce light; deep but transparent shadows, creamy rolled-off highlights, gentle natural vignette. Forms and materials: sculptural curves (spiral stairs, arched openings, rounded plaster walls), solid oak and walnut joinery, travertine floors, bouclé and linen upholstery in oatmeal and ivory, an olive tree in a large matte planter, very few objects. Camera: full-frame architectural photography, 24–35 mm for interiors, verticals perfectly corrected, eye level around 1.4 m, f/5.6 with soft depth falloff, fine natural film grain, photorealistic. Grade: warm, low saturation, slightly lifted blacks, brown-gold midtones, cohesive across the whole set.

Avoid: cold or blue cast, neon, glossy CGI render look, plastic surfaces, oversaturation, HDR halos, harsh flash, clutter, visible logos or brand names, any text or lettering, watermark, signature, distorted or bent vertical lines, warped perspective, extra or merged stair treads, impossible geometry, floating furniture, duplicated objects, people (unless requested), malformed hands or fingers.
```
</details>

### V2 · S4 Dòng biệt thự
- Lưu ảnh gốc: `assets/raw/V2.png` · Tỉ lệ **4:3**
- Series: `VILLA_SERIES`
- Kiểm tra sau khi tạo: Phần console hợp lý kết cấu

**Cảnh:** Villa type 'Tùng Lâm': a two-storey hillside villa whose upper volume cantilevers over the slope among tall pines, a suspended oak-floored terrace with a thin bronze railing.

**Bố cục:** Slope falling from left to right.

<details><summary>Prompt cuối cùng (đã ghép)</summary>

```text
Villa type 'Tùng Lâm': a two-storey hillside villa whose upper volume cantilevers over the slope among tall pines, a suspended oak-floored terrace with a thin bronze railing.

COMPOSITION — Slope falling from left to right.

SERIES LOCK (identical across V1–V4) — same photographic setup for every image: camera 1.6 m high in the front garden, 35 mm, three-quarter front view, villa occupying the central 70% of the frame, golden hour sun from the left at 15° elevation, the same soft peach-to-dusty-rose sky, the same pine forest backdrop, warm light glowing from inside every window, a strip of manicured lawn and low ornamental grasses in the foreground. Architecture language shared by all: low horizontal massing, warm limewash and travertine walls, deep eaves clad in oak slats, large arched openings, bronze-framed glazing, flat roofs with thin edges.

STYLE DNA — warm luxury architectural and interior photography for a high-end residential brand, editorial and quiet, like a spread in a premium design magazine. Palette: espresso brown (#2A1F17), warm walnut, honey-toned solid white oak, travertine and limewash cream (#F3EBE2), caramel accents (#CFAE86), thin matte-black metal, a little brushed bronze; greens only from real foliage (olive trees, pines), always muted. Light: low golden sun raking through tall glass, warm 2700K concealed LED lines under stair treads and in ceiling coves, soft bounce light; deep but transparent shadows, creamy rolled-off highlights, gentle natural vignette. Forms and materials: sculptural curves (spiral stairs, arched openings, rounded plaster walls), solid oak and walnut joinery, travertine floors, bouclé and linen upholstery in oatmeal and ivory, an olive tree in a large matte planter, very few objects. Camera: full-frame architectural photography, 24–35 mm for interiors, verticals perfectly corrected, eye level around 1.4 m, f/5.6 with soft depth falloff, fine natural film grain, photorealistic. Grade: warm, low saturation, slightly lifted blacks, brown-gold midtones, cohesive across the whole set.

Avoid: cold or blue cast, neon, glossy CGI render look, plastic surfaces, oversaturation, HDR halos, harsh flash, clutter, visible logos or brand names, any text or lettering, watermark, signature, distorted or bent vertical lines, warped perspective, extra or merged stair treads, impossible geometry, floating furniture, duplicated objects, people (unless requested), malformed hands or fingers.
```
</details>

### V3 · S4 Dòng biệt thự
- Lưu ảnh gốc: `assets/raw/V3.png` · Tỉ lệ **4:3**
- Series: `VILLA_SERIES`
- Kiểm tra sau khi tạo: Hai căn đối xứng chuẩn

**Cảnh:** Villa type 'Song Mộc': a pair of mirrored two-storey semi-detached villas joined by a shared travertine garden wall, each with its own arched entrance and a young olive tree, a shared lawn between them.

**Bố cục:** Perfect bilateral symmetry around the shared wall.

<details><summary>Prompt cuối cùng (đã ghép)</summary>

```text
Villa type 'Song Mộc': a pair of mirrored two-storey semi-detached villas joined by a shared travertine garden wall, each with its own arched entrance and a young olive tree, a shared lawn between them.

COMPOSITION — Perfect bilateral symmetry around the shared wall.

SERIES LOCK (identical across V1–V4) — same photographic setup for every image: camera 1.6 m high in the front garden, 35 mm, three-quarter front view, villa occupying the central 70% of the frame, golden hour sun from the left at 15° elevation, the same soft peach-to-dusty-rose sky, the same pine forest backdrop, warm light glowing from inside every window, a strip of manicured lawn and low ornamental grasses in the foreground. Architecture language shared by all: low horizontal massing, warm limewash and travertine walls, deep eaves clad in oak slats, large arched openings, bronze-framed glazing, flat roofs with thin edges.

STYLE DNA — warm luxury architectural and interior photography for a high-end residential brand, editorial and quiet, like a spread in a premium design magazine. Palette: espresso brown (#2A1F17), warm walnut, honey-toned solid white oak, travertine and limewash cream (#F3EBE2), caramel accents (#CFAE86), thin matte-black metal, a little brushed bronze; greens only from real foliage (olive trees, pines), always muted. Light: low golden sun raking through tall glass, warm 2700K concealed LED lines under stair treads and in ceiling coves, soft bounce light; deep but transparent shadows, creamy rolled-off highlights, gentle natural vignette. Forms and materials: sculptural curves (spiral stairs, arched openings, rounded plaster walls), solid oak and walnut joinery, travertine floors, bouclé and linen upholstery in oatmeal and ivory, an olive tree in a large matte planter, very few objects. Camera: full-frame architectural photography, 24–35 mm for interiors, verticals perfectly corrected, eye level around 1.4 m, f/5.6 with soft depth falloff, fine natural film grain, photorealistic. Grade: warm, low saturation, slightly lifted blacks, brown-gold midtones, cohesive across the whole set.

Avoid: cold or blue cast, neon, glossy CGI render look, plastic surfaces, oversaturation, HDR halos, harsh flash, clutter, visible logos or brand names, any text or lettering, watermark, signature, distorted or bent vertical lines, warped perspective, extra or merged stair treads, impossible geometry, floating furniture, duplicated objects, people (unless requested), malformed hands or fingers.
```
</details>

### V4 · S4 Dòng biệt thự
- Lưu ảnh gốc: `assets/raw/V4.png` · Tỉ lệ **4:3**
- Series: `VILLA_SERIES`
- Kiểm tra sau khi tạo: Đúng 7 vòm đều nhau

**Cảnh:** Villa type 'Đại Viên': a grand two-storey mansion arranged around a courtyard, a long arched loggia of seven arches across the front, a central reflecting pool in the forecourt, mature olive trees in large stone planters.

**Bố cục:** Loggia centred, forecourt pool in the lower third.

<details><summary>Prompt cuối cùng (đã ghép)</summary>

```text
Villa type 'Đại Viên': a grand two-storey mansion arranged around a courtyard, a long arched loggia of seven arches across the front, a central reflecting pool in the forecourt, mature olive trees in large stone planters.

COMPOSITION — Loggia centred, forecourt pool in the lower third.

SERIES LOCK (identical across V1–V4) — same photographic setup for every image: camera 1.6 m high in the front garden, 35 mm, three-quarter front view, villa occupying the central 70% of the frame, golden hour sun from the left at 15° elevation, the same soft peach-to-dusty-rose sky, the same pine forest backdrop, warm light glowing from inside every window, a strip of manicured lawn and low ornamental grasses in the foreground. Architecture language shared by all: low horizontal massing, warm limewash and travertine walls, deep eaves clad in oak slats, large arched openings, bronze-framed glazing, flat roofs with thin edges.

STYLE DNA — warm luxury architectural and interior photography for a high-end residential brand, editorial and quiet, like a spread in a premium design magazine. Palette: espresso brown (#2A1F17), warm walnut, honey-toned solid white oak, travertine and limewash cream (#F3EBE2), caramel accents (#CFAE86), thin matte-black metal, a little brushed bronze; greens only from real foliage (olive trees, pines), always muted. Light: low golden sun raking through tall glass, warm 2700K concealed LED lines under stair treads and in ceiling coves, soft bounce light; deep but transparent shadows, creamy rolled-off highlights, gentle natural vignette. Forms and materials: sculptural curves (spiral stairs, arched openings, rounded plaster walls), solid oak and walnut joinery, travertine floors, bouclé and linen upholstery in oatmeal and ivory, an olive tree in a large matte planter, very few objects. Camera: full-frame architectural photography, 24–35 mm for interiors, verticals perfectly corrected, eye level around 1.4 m, f/5.6 with soft depth falloff, fine natural film grain, photorealistic. Grade: warm, low saturation, slightly lifted blacks, brown-gold midtones, cohesive across the whole set.

Avoid: cold or blue cast, neon, glossy CGI render look, plastic surfaces, oversaturation, HDR halos, harsh flash, clutter, visible logos or brand names, any text or lettering, watermark, signature, distorted or bent vertical lines, warped perspective, extra or merged stair treads, impossible geometry, floating furniture, duplicated objects, people (unless requested), malformed hands or fingers.
```
</details>

### B1 · S4 Banner hoàn thiện riêng
- Lưu ảnh gốc: `assets/raw/B1.png` · Tỉ lệ **21:9**
- Kiểm tra sau khi tạo: Bản vẽ không có chữ đọc được · Nửa trái gần như đen

**Cảnh:** An architect's oak desk at dusk seen at a low oblique angle: large sheets of villa floor plans drawn in fine graphite lines, a brass drafting compass, a small solid-oak architectural model of an arched villa, rolled drawings tied with linen string, a warm brass desk lamp casting a pool of light on the right.

**Bố cục:** Ultra-wide 21:9; all detail and light in the right 50%; the left half falls into near-black warm brown shadow with almost no detail (text and icons sit there).

<details><summary>Prompt cuối cùng (đã ghép)</summary>

```text
An architect's oak desk at dusk seen at a low oblique angle: large sheets of villa floor plans drawn in fine graphite lines, a brass drafting compass, a small solid-oak architectural model of an arched villa, rolled drawings tied with linen string, a warm brass desk lamp casting a pool of light on the right.

COMPOSITION — Ultra-wide 21:9; all detail and light in the right 50%; the left half falls into near-black warm brown shadow with almost no detail (text and icons sit there).

STYLE DNA — warm luxury architectural and interior photography for a high-end residential brand, editorial and quiet, like a spread in a premium design magazine. Palette: espresso brown (#2A1F17), warm walnut, honey-toned solid white oak, travertine and limewash cream (#F3EBE2), caramel accents (#CFAE86), thin matte-black metal, a little brushed bronze; greens only from real foliage (olive trees, pines), always muted. Light: low golden sun raking through tall glass, warm 2700K concealed LED lines under stair treads and in ceiling coves, soft bounce light; deep but transparent shadows, creamy rolled-off highlights, gentle natural vignette. Forms and materials: sculptural curves (spiral stairs, arched openings, rounded plaster walls), solid oak and walnut joinery, travertine floors, bouclé and linen upholstery in oatmeal and ivory, an olive tree in a large matte planter, very few objects. Camera: full-frame architectural photography, 24–35 mm for interiors, verticals perfectly corrected, eye level around 1.4 m, f/5.6 with soft depth falloff, fine natural film grain, photorealistic. Grade: warm, low saturation, slightly lifted blacks, brown-gold midtones, cohesive across the whole set.

Avoid: cold or blue cast, neon, glossy CGI render look, plastic surfaces, oversaturation, HDR halos, harsh flash, clutter, visible logos or brand names, any text or lettering, watermark, signature, distorted or bent vertical lines, warped perspective, extra or merged stair treads, impossible geometry, floating furniture, duplicated objects, people (unless requested), malformed hands or fingers.
```
</details>

### F1 · S5 Lời mời
- Lưu ảnh gốc: `assets/raw/F1.png` · Tỉ lệ **16:9**
- Block: `BLEND_CREAM`
- Kiểm tra sau khi tạo: Nền kem phẳng, khớp màu thẻ #F7F1EC · Hai bên trống

**Cảnh:** Minimal still life: a round, hand-thrown textured stoneware vase in warm sand tone holding a few dried olive and wildflower branches with tiny pale seed heads, standing on a slim floating oak shelf. Soft daylight from the upper left, a very soft long shadow on the wall.

**Bố cục:** 16:9, vase and branches centred and occupying the middle 30% of the width; shelf in the lower quarter; everything else is empty cream wall.

<details><summary>Prompt cuối cùng (đã ghép)</summary>

```text
Minimal still life: a round, hand-thrown textured stoneware vase in warm sand tone holding a few dried olive and wildflower branches with tiny pale seed heads, standing on a slim floating oak shelf. Soft daylight from the upper left, a very soft long shadow on the wall.

COMPOSITION — 16:9, vase and branches centred and occupying the middle 30% of the width; shelf in the lower quarter; everything else is empty cream wall.

BACKGROUND — the background is a flat, evenly lit warm cream limewash wall (#F2EBE4) with no texture variation near the edges, so the photo can melt seamlessly into a cream web card; generous empty space on both sides.

STYLE DNA — warm luxury architectural and interior photography for a high-end residential brand, editorial and quiet, like a spread in a premium design magazine. Palette: espresso brown (#2A1F17), warm walnut, honey-toned solid white oak, travertine and limewash cream (#F3EBE2), caramel accents (#CFAE86), thin matte-black metal, a little brushed bronze; greens only from real foliage (olive trees, pines), always muted. Light: low golden sun raking through tall glass, warm 2700K concealed LED lines under stair treads and in ceiling coves, soft bounce light; deep but transparent shadows, creamy rolled-off highlights, gentle natural vignette. Forms and materials: sculptural curves (spiral stairs, arched openings, rounded plaster walls), solid oak and walnut joinery, travertine floors, bouclé and linen upholstery in oatmeal and ivory, an olive tree in a large matte planter, very few objects. Camera: full-frame architectural photography, 24–35 mm for interiors, verticals perfectly corrected, eye level around 1.4 m, f/5.6 with soft depth falloff, fine natural film grain, photorealistic. Grade: warm, low saturation, slightly lifted blacks, brown-gold midtones, cohesive across the whole set.

Avoid: cold or blue cast, neon, glossy CGI render look, plastic surfaces, oversaturation, HDR halos, harsh flash, clutter, visible logos or brand names, any text or lettering, watermark, signature, distorted or bent vertical lines, warped perspective, extra or merged stair treads, impossible geometry, floating furniture, duplicated objects, people (unless requested), malformed hands or fingers.
```
</details>

## 6. Tiêu chí duyệt ảnh (chấm 1–5, cần ≥ 4 ở mọi mục)

| Tiêu chí | Câu hỏi |
|---|---|
| Ánh sáng | Có phải nắng chiều ấm, bóng trong, highlight mềm không? |
| Vật liệu | Gỗ sồi mật ong, travertine, vôi kem, kim loại đen mảnh. Có lẫn vật liệu lạ không? |
| Bố cục | Có chừa đúng vùng cho chữ như yêu cầu không? |
| Hình học | Đường đứng có thẳng không? Bậc thang, vòm, hồ bơi có hợp lý không? |
| Đồng bộ | Đặt cạnh H1 có thấy cùng một buổi chụp không? |
| Sạch | Có chữ, logo, watermark hay vật thừa không? |
