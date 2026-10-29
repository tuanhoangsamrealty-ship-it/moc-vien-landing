# Playbook · Landing page biệt thự phong cách "FORMA" — dự án concept **Mộc Viên**

> Tài liệu gốc của bộ kit. Đọc để hiểu **vì sao** trang được làm như vậy; muốn **làm ngay** thì xem `START_HERE.md`.
> Ảnh tham chiếu: `docs/reference/reference-forma-stairs.jpg` (landing một thương hiệu cầu thang cao cấp).
> Bộ prompt ảnh: `docs/02_IMAGE_PROMPTS.md` (nguồn chuẩn: `prompts/images.json`).

**Nhãn:** `[ĐO]` đo trực tiếp từ ảnh tham chiếu · `[SUY]` suy luận · `[MẪU]` số liệu minh hoạ của dự án concept.

---

## 1. Giải mã mẫu tham chiếu

### 1.1 Giải phẫu trang (7 khối)

| # | Khối | Bố cục | Vai trò |
|---|---|---|---|
| 1 | **Hero** | Ảnh nội thất toàn màn hình; nửa trái tối chứa tiêu đề serif 3 dòng (1 từ viết tay màu caramel), đoạn mô tả, nút pill caramel, hàng 3 icon nét mảnh | Gây ấn tượng bằng ánh sáng và vật liệu |
| 2 | **Câu chuyện** | Thẻ kem **đè lên mép dưới hero**; ảnh bàn tay nghệ nhân bên trái, tiêu đề + đoạn văn + 4 số liệu bên phải | Chuyển từ "đẹp" sang "đáng tin" |
| 3 | **Danh mục** | Tiêu đề trái + link phải; 4 thẻ sản phẩm cùng một kiểu chụp | Cho khách chọn |
| 4 | **Banner thiết kế riêng** | Thẻ nâu đậm bo góc, ảnh bản vẽ mờ phía phải, 3 bước có icon | Nâng giá trị: "làm riêng cho bạn" |
| 5 | **Blog** | 3 thẻ ngang | Nuôi dưỡng (bỏ trong bản biệt thự) |
| 6 | **Hỗ trợ / form** | Thẻ kem: chữ trái, **ảnh tĩnh vật tan vào nền** ở giữa, form phải; thẻ đè lên footer | Chốt hành động |
| 7 | **Footer** | Nâu espresso, logo, 3 cột link, cột liên hệ, nút viền | Đóng trang |

### 1.2 Hệ thị giác đo được

| Thuộc tính | Giá trị | Ghi chú |
|---|---|---|
| Nền trang | `#F6EFE9` `[ĐO]` | kem ấm, không phải trắng |
| Nền thẻ | `#FAF5F1` `[ĐO]` | sáng hơn nền 1 bậc → thẻ "nổi" mà không cần viền |
| Nâu đậm (hero, banner) | `#2A1F17` / `#3A2E25` `[ĐO]` | |
| Footer | `#32281F` `[ĐO]` | |
| Caramel (nút, chữ viết tay, icon) | ≈ `#CFAE86`, đậm `#A9875F` `[ĐO]` | màu nhấn duy nhất |
| Chữ | `#251B12`, phụ `#6E625A` `[ĐO]` | không dùng đen thuần |
| Tiêu đề | serif tương phản vừa, nét thường (≈400) `[SUY]` | |
| Chữ nhấn | 1 từ viết tay (script) màu caramel, to hơn chữ thường ~30% | chữ ký thị giác của mẫu |
| Chữ thân | sans hình học, 12–15px | |
| Bo góc | thẻ lớn ~20px, ảnh trong thẻ ~12px, nút pill tròn | |
| Bóng | rất mềm, lan rộng, gần như không thấy viền | |

### 1.3 Ngôn ngữ ảnh

Toàn bộ ảnh như cùng **một buổi chụp**: nắng chiều vàng, gỗ sồi màu mật ong, travertine, tường vôi kem, kim loại đen nét mảnh, cây ô-liu trong chậu đen, nội thất bouclé/lanh. Đường cong là motif xuyên suốt (cầu thang xoắn, tay vịn cong). Người chỉ xuất hiện qua **bàn tay**.

---

## 2. Tám điểm khó và cách giải

| # | Điểm khó | Vì sao khó | Cách giải trong kit |
|---|---|---|---|
| 1 | **Cả bộ ảnh "một giọng"** | AI sinh từng ảnh độc lập nên lệch màu, lệch ánh sáng, lệch vật liệu | Khối **STYLE DNA** ghép vào mọi prompt · tạo **H1 trước** rồi dùng làm ảnh tham chiếu phong cách · **SERIES LOCK** cho nhóm ảnh cùng loại · grade chung trong `process_images.py` |
| 2 | **Hero không cần lớp phủ mà chữ vẫn đọc rõ** | Mẫu dựa vào việc *ảnh được chụp tối sẵn ở bên trái*. Ảnh AI thường sáng đều | Block `TEXT_SPACE_LEFT` ép 42% bên trái tối (luma < 20%) · script **đo độ sáng** vùng chữ và cảnh báo · CSS vẫn có gradient dự phòng |
| 3 | **Serif + chữ viết tay có dấu tiếng Việt** | Rất ít font script có bộ dấu; dấu chồng (ộ, ễ) dễ đâm vào dòng trên | Đã test thực tế: **Newsreader** (serif) + **Allura** (script) + **Manrope** (thân) đều có subset Vietnamese và hiển thị dấu sạch. Cormorant Garamond bị loại vì dấu mũ cao nhọn ở cỡ lớn |
| 4 | **Lớp chồng tinh tế** | Thẻ đè hero, thẻ form đè footer, banner tối trong nền kem. Làm vụng sẽ thấy lệch hoặc bẩn | Thẻ câu chuyện `margin-top:-140px` + chuyển động "nhấc lên"; nền section form chia 62% kem / 38% nâu |
| 5 | **Mật độ cao nhưng vẫn sang** | Mẫu có rất nhiều thành phần nhỏ | Lưới 1320px, khoảng cách theo thang cố định, chỉ một màu nhấn, chữ thân nhỏ màu nâu xám, không dùng đen |
| 6 | **Bàn tay người** | AI hay vẽ sai số ngón và khớp | Block `HANDS`: đúng 5 ngón, da sáng đều, không lộ mặt; checklist riêng cho ảnh S2 |
| 7 | **Ảnh tĩnh vật tan vào thẻ** | Nền ảnh phải trùng màu thẻ, nếu lệch sẽ lộ "hộp ảnh" | Block `BLEND_CREAM` yêu cầu nền kem phẳng · CSS `mask-image` làm mờ hai mép ảnh |
| 8 | **Từ sản phẩm (cầu thang) sang bất động sản** | Danh mục có giá, banner "thiết kế riêng" cần được dịch nghĩa | Danh mục → **4 dòng biệt thự**; banner → **hoàn thiện nội thất theo dấu ấn riêng**; blog → bỏ, nhường chỗ cho **gallery không gian** |

---

## 3. Chuyển dịch sang dự án biệt thự

**Dự án concept:** **Mộc Viên Residences** — 48 biệt thự đồi thông ven hồ `[MẪU]`. "Mộc" (gỗ) nối thẳng với tinh thần thủ công của mẫu; "Viên" (khu vườn, dinh cơ) cho cảm giác biệt lập. Tên hai âm tiết rất hợp với cách tách **serif + script**: "Mộc *Viên*".

> Đây là dự án **minh hoạ thiết kế**. Footer luôn hiện ghi chú concept khi `is_concept: true`. Muốn dùng cho dự án thật: xem mục 7.

### Mạch truyện 5 section

| Section | Câu hỏi của khách | Cảm xúc | Chuyển động chủ đạo (mỗi section chỉ một) |
|---|---|---|---|
| **S1 Hero — Ánh sáng** | "Nơi này là gì?" | Ngỡ ngàng | **Vệt nắng** quét qua tên dự án; chữ "Viên" được **viết ra** |
| **S2 Câu chuyện — Bàn tay** | "Vì sao đáng tin?" | Tin tưởng | Thẻ **nhấc lên** che dần hero; ảnh mở như **một đường bào gỗ** |
| **S3 Không gian — gallery chủ đạo** | "Sống ở đó ra sao?" | Khao khát | **Ô cửa vòm** nở ra toàn màn hình → đi qua **6 căn phòng** |
| **S4 Dòng biệt thự — Lựa chọn** | "Tôi chọn căn nào?" | Cân nhắc | Thẻ **xếp lên bàn**; icon **tự vẽ nét** |
| **S5 Lời mời** | "Bước tiếp theo?" | Quyết định | Thẻ cuối nổi lên êm; bình gốm tiến lại gần |

Nhịp màu nền: nâu tối (S1) → kem (S2) → kem rồi tối dần trong vòm (S3) → kem + banner tối (S4) → kem chạm footer nâu (S5). Người xem đi **từ trong nhà ra vườn rồi quay lại bàn tư vấn**.

---

## 4. Hệ thiết kế (token dùng trong template)

### 4.1 Màu — khai báo trong `project.config.json → brand.colors`
`espresso #2A1F17` · `espresso_2 #3A2E25` · `footer #32281F` · `cream #F6EFE9` · `card #FAF5F1` · `card_line #ECE2D8` · `caramel #CFAE86` · `caramel_deep #A9875F` · `ink #251B12` · `ink_soft #6E625A` · `on_dark #F3ECE4`

Quy tắc: caramel là **màu nhấn duy nhất**. Không dùng xanh lá hay xanh dương cho UI; màu xanh chỉ đến từ cây trong ảnh.

### 4.2 Chữ

| Vai trò | Font | Cỡ desktop | Ghi chú |
|---|---|---|---|
| Tên dự án (H1) | Newsreader 400 + **Allura** | `clamp(76px,10vw,160px)`; phần script ×1.3 | Cụm **nổi bật nhất trang**; "Mộc" serif kem, "Viên" script caramel |
| Tagline hero | Newsreader 300 | 23–36px | 2 dòng |
| Tiêu đề section | Newsreader 400 | 32–44px | 1 cụm `<em>` = chữ script, tối đa 1 cụm mỗi màn hình |
| Số liệu | Newsreader 400 | 30–42px | |
| Thân | Manrope 400 | 13.5–15px, line-height 1.65–1.72 | màu `ink_soft` trên nền kem |
| Nhãn / eyebrow | Manrope 500 | 11.5px, hoa, giãn chữ .2em | màu caramel |

### 4.3 Lưới & thành phần
- Khung 1320px, lề `clamp(16px, 4.2vw, 60px)`.
- Bo góc: thẻ lớn 22px · thẻ vừa 16px · ảnh trong thẻ 12px · nút pill 999px.
- Bóng: `0 30px 60px -34px rgba(42,31,23,.32)`.
- **Nút pill caramel:** chữ đậm vừa, có vòng tròn nâu chứa mũi tên ở cuối (giống mẫu).
- **Nút nav:** pill nâu `espresso_2`.
- **Icon:** nét mảnh 1.2px, màu caramel, vẽ bằng SVG (lá, cây thông, chìa khoá, compa, khối 3D, ngôi nhà).

---

## 5. Năm section — nội dung, thị giác, chuyển động

Toàn bộ chữ nằm trong `content/content.json`; dưới đây là bản thiết kế.

### S1 · Hero — "Ánh sáng"

**Nội dung**
- Eyebrow: *Biệt thự đồi thông ven hồ · Bộ sưu tập 2027*
- **H1: Mộc *Viên***
- Tagline: *Biệt thự nơi gỗ, đá và ánh sáng / định hình ngôi nhà của bạn*
- Thân: *Bốn mươi tám biệt thự trên sườn đồi thông, nhìn xuống mặt hồ…*
- CTA: **Xem bộ sưu tập** · 3 icon: *Gỗ sồi & đá travertine tự nhiên* / *70% cây xanh và mặt nước* / *Bàn giao nội thất hoàn thiện thủ công*

**Thị giác:** ảnh H1 (sảnh thông tầng, cầu thang xoắn gỗ sồi bên phải, nửa trái tối). Lớp phủ gradient từ trái làm dự phòng. Trên mobile dùng ảnh **H1M** (dọc 4:5, nửa trên tối).

**Chuyển động**

| Lúc | Đối tượng | Hiệu ứng |
|---|---|---|
| 0s | Ảnh | `scale 1.12 → 1`, 2.8s `expo.out` — ảnh "mở mắt" |
| .45s | "Mộc" | trồi lên từ mặt nạ, 1.3s `power4.out` |
| .85s | "Viên" (script) | `clip-path` quét trái → phải 1.6s — như được **viết** |
| .9s | Vệt nắng | dải sáng ấm `soft-light` lướt chéo qua tên, 2.2s, rồi tan |
| 1.25s | Tagline, thân, CTA, icon | fade + trồi 18px, so le .08s |
| Cuộn 0 → 100vh | Ảnh / lớp tối / nội dung | ảnh trôi xuống 12% · tối dần tới .45 · nội dung đi lên và mờ |

### S2 · Câu chuyện — "Bàn tay"

**Nội dung:** *Câu chuyện Mộc Viên* — *ngôi nhà đẹp nhất là ngôi nhà được làm bằng tay…* · 4 số liệu `[MẪU]`: **48** biệt thự · **12 ha** · **18%** mật độ xây dựng · **70%** cây xanh và mặt nước.

**Thị giác:** thẻ kem đè lên hero 140px; ảnh **S2** bàn tay nghệ nhân chà nhẵn tay vịn gỗ cong (nối với cầu thang ở hero).

**Chuyển động**
- Khi hero cuộn đi: thẻ `y 110 → 0` (scrub) — thẻ **nhấc lên** che dần hero.
- Khi thẻ vào khung nhìn: ảnh `clip-path inset(0 100% 0 0) → 0` trong 1.5s, kèm `scale 1.18 → 1` — như **một nhát bào**. Tiêu đề trồi lên, gạch caramel 56px kéo dài, đoạn văn và số liệu so le, số liệu đếm lên.

### S3 · Không gian — gallery chủ đạo ★

**Nội dung:** eyebrow *Bộ sưu tập không gian* · tiêu đề *Bước vào / một ngôi nhà / **biết thở*** · gợi ý *Cuộn xuống để bước qua ô cửa vòm…* · chú thích *Mộc Viên lúc hoàng hôn* · tiêu đề chặng 2 *Sáu không gian, một nhịp sống* · 6 thẻ phòng (tên, vật liệu, một câu):

| # | Phòng | Vật liệu | Câu |
|---|---|---|---|
| 01 | Sảnh thông tầng | Gỗ sồi · Travertine · Kính | Nơi ánh sáng đi xuống theo từng bậc thang. |
| 02 | Bếp & bàn đảo | Travertine · Óc chó · Đồng | Một khối đá nguyên, một bữa sáng chậm. |
| 03 | Thư viện | Óc chó · Da · Đèn hắt | Những buổi chiều dành cho trang sách. |
| 04 | Phòng ngủ master | Lanh · Sồi trắng · Tầm hồ | Thức dậy cùng màn sương trên mặt hồ. |
| 05 | Phòng tắm spa | Travertine · Đá đen · Đồng | Bồn đá, ánh nến, và sự tĩnh lặng. |
| 06 | Hiên & hồ bơi | Teak · Đá tự nhiên · Hoàng hôn | Mặt nước nối liền với mặt hồ phía xa. |

**Thị giác & cơ chế (desktop):** section được **ghim** trong `1.3 × chiều cao màn hình + quãng trượt ngang`.

| Tiến trình | Diễn biến |
|---|---|
| 0 → 30% | Ô vòm `inset(15% 36.5% 9% 36.5% round 600px 600px 26px 26px)` **nở** thành toàn màn hình; ảnh G0 `scale 1.25 → 1`; tiêu đề và gợi ý mờ đi |
| 24 → 34% | Chú thích "lúc hoàng hôn" hiện rồi tắt; lớp tối phủ lên ảnh |
| 33 → 100% | Tiêu đề chặng 2 + bộ đếm `01/06` hiện; dải 6 thẻ phòng trượt từ phải sang trái, mỗi thẻ rơi nhẹ vào chỗ (`y 50`, `rotate 1.5°`); ảnh nền trôi ngược 6%; thanh tiến trình caramel chạy |

**Ý nghĩa:** ô cửa vòm là "cánh cửa" bước vào nhà. Nền chuyển từ kem sang tối giống bước từ ngoài sáng vào trong nhà. Sau đó khách đi qua từng phòng theo thứ tự sinh hoạt.

**Mobile:** không ghim. Ô vòm mở rộng theo cuộn (scrub). Thẻ phòng cuộn ngang bằng tay (scroll-snap) trên nền tối.

### S4 · Dòng biệt thự — "Lựa chọn"

**Nội dung:** 4 thẻ `[MẪU]` — Đơn lập «Ven Hồ» (*từ 38 tỷ*) · Sườn đồi «Tùng Lâm» (*từ 32 tỷ*) · Song lập «Song Mộc» (*từ 24 tỷ*) · Dinh thự «Đại Viên» (*từ 85 tỷ*); dòng chú thích *Giá minh hoạ cho dự án concept*. Banner: *Hoàn thiện theo **dấu ấn** riêng* + 3 bước (*Khảo sát & tư vấn riêng* · *Phối cảnh 3D nội thất* · *Bàn giao trọn gói*) + CTA *Nhận tư vấn thiết kế*.

**Thị giác:** 4 ảnh V1–V4 **cùng một kiểu chụp** (SERIES LOCK), nên lưới thẻ trông như một catalogue. Banner nền nâu, ảnh bản vẽ **B1** chìm ở bên phải.

**Chuyển động:** thẻ `y 70 → 0` so le .1s; khi hover thẻ nhấc 6px, ảnh zoom 1.06, nút tròn xoay −45° và chuyển màu caramel. Ảnh banner trôi parallax ±8%. Icon 3 bước **tự vẽ nét** bằng `stroke-dashoffset`, so le .06s.

### S5 · Lời mời

**Nội dung:** *Cần tư vấn chọn căn phù hợp?* · đoạn mô tả · form: số điện thoại + nút *Gửi yêu cầu* + ô đồng ý · trạng thái thành công / lỗi.

**Thị giác:** thẻ 3 cột; ảnh **F1** (bình gốm, cành khô, nền kem) ở giữa, hai mép làm mờ bằng `mask-image` để ảnh tan vào thẻ; thẻ đè lên footer.

**Chuyển động:** thẻ nổi lên `y 60 → 0`; ảnh `scale 1.1 → 1` theo cuộn. Ô nhập có viền caramel và quầng sáng khi focus.

**Form:** kiểm tra định dạng số điện thoại Việt Nam và ô đồng ý. Nếu `contact.form_endpoint` có giá trị (Google Apps Script, Make, n8n…), dữ liệu được POST tới đó.

---

## 6. Ngữ pháp chuyển động chung

1. **Mỗi section chỉ một chuyển động chủ đạo**; mọi thứ khác nhỏ và nhanh.
2. **Chuyển động phải mang nghĩa:** nắng = mở đầu, viết = dấu tay, nhấc thẻ = trang mới, bào gỗ = thủ công, cửa vòm = bước vào, xếp thẻ = lựa chọn.
3. **Người xem cầm lái:** chuyển động theo cuộn gắn với scroll (scrub); không tự chạy âm thanh; chỉ ghim một section (S3).

- Easing: vào `power3/4.out`, `expo.out`; quét `power2.inOut`; theo cuộn dùng `none`.
- Thời lượng: nhỏ .3–.5s · reveal .9–1.3s · hero 2.2–2.8s.
- Thư viện: GSAP 3.13 + ScrollTrigger + Lenis 1.3.4 (link cố định phiên bản trong config).
- Chỉ animate `transform`, `opacity`, `clip-path`, `stroke-dashoffset`.
- **Giảm chuyển động** (`prefers-reduced-motion`): tắt Lenis, tắt ghim, tắt scrub; gallery chuyển thành cuộn ngang thường.
- **Mobile (< 768px):** ảnh hero dọc riêng, không ghim, thẻ phòng cuộn ngang bằng tay, ẩn 3 icon hero.

---

## 7. Quy tắc trung thực (bắt buộc)

- `is_concept: true` → footer hiện ghi chú concept, danh mục hiện *Giá minh hoạ*. Không gỡ khi đăng.
- **Dự án THẬT** (`is_concept: false`):
  - Ảnh có `product: true` (G0, V1–V4 — mặt tiền, sản phẩm) **phải** là phối cảnh hoặc ảnh chụp chính thức. Đặt file vào `assets/raw/<ID>.jpg`; script sẽ **không** tự tạo những ảnh này (trừ khi chạy `--allow-product-ai` cho bản nháp nội bộ).
  - Ảnh AI chỉ dùng cho không khí, nội thất gợi ý, chi tiết vật liệu, và cần ghi rõ "hình ảnh minh hoạ".
  - Mọi số liệu và giá lấy từ tài liệu bán hàng chính thức; thay toàn bộ `[Cập nhật …]`.
- Không dùng khuôn mặt AI như cư dân hay khách hàng thật.

---

## 8. Checklist QA

**Ảnh**
- [ ] 16 ảnh đặt cạnh nhau: cùng nhiệt độ màu, cùng độ tương phản, cùng ngôn ngữ vật liệu
- [ ] H1: nửa trái tối (`check.py` báo luma ≤ .30); cầu thang không có bậc thừa hay méo
- [ ] S2: đúng 5 ngón mỗi bàn tay, da sáng đều, không lộ mặt
- [ ] V1–V4: cùng góc máy, cùng bầu trời, cùng giờ chụp
- [ ] F1: nền trùng màu thẻ, không lộ mép

**Chữ & nội dung**
- [ ] Tên dự án là cụm lớn nhất trang; dấu tiếng Việt không đâm vào nhau ở mọi cỡ
- [ ] Không còn `[Cập nhật …]` khi đăng thật
- [ ] Ghi chú concept / nguồn số liệu đúng trạng thái dự án

**Chuyển động & kỹ thuật**
- [ ] Ô vòm nở đều hai bên; bộ đếm 01→06 khớp thẻ
- [ ] Không lỗi console; reduced-motion hoạt động; mobile không bị cuộn ngang toàn trang
- [ ] LCP < 2.5s trên 4G (ảnh hero ≤ 400 KB)
