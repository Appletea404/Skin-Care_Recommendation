import subprocess
import tempfile
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = BASE_DIR / "presentation_png"
CHROME = "/usr/bin/google-chrome"
WIDTH = 1920
HEIGHT = 1080


STYLE = """
@font-face {
  font-family: NotoCJK;
  src: url("file:///usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc");
}
@font-face {
  font-family: NotoCJK;
  src: url("file:///usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc");
  font-weight: 800;
}
* { box-sizing: border-box; }
body {
  width: 1920px;
  height: 1080px;
  margin: 0;
  overflow: hidden;
  font-family: NotoCJK, Arial, sans-serif;
  color: #291c22;
  background: #fff8f6;
}
.slide {
  position: relative;
  width: 1920px;
  height: 1080px;
  padding: 82px 98px 72px;
  overflow: hidden;
  background:
    radial-gradient(circle at 92% 8%, rgba(193, 38, 78, .16), transparent 330px),
    radial-gradient(circle at 5% 100%, rgba(214, 107, 61, .13), transparent 420px),
    linear-gradient(135deg, #fffaf8 0%, #fff1f3 54%, #fff7ee 100%);
}
.slide::after {
  content: "";
  position: absolute;
  inset: 34px;
  border: 2px solid rgba(146, 36, 62, .12);
  border-radius: 42px;
  pointer-events: none;
}
.kicker {
  font-size: 23px;
  letter-spacing: 8px;
  text-transform: uppercase;
  color: #9c2444;
  font-weight: 800;
}
h1 {
  margin: 20px 0 0;
  font-size: 92px;
  line-height: 1.06;
  letter-spacing: 0;
  color: #431421;
}
.subtitle {
  margin-top: 22px;
  font-size: 34px;
  color: #76525e;
}
.brand {
  position: absolute;
  right: 104px;
  bottom: 74px;
  font-size: 22px;
  font-weight: 800;
  color: #8d5264;
  letter-spacing: 3px;
}
.chip-row { display: flex; gap: 18px; flex-wrap: wrap; margin-top: 38px; }
.chip {
  padding: 15px 26px;
  border-radius: 999px;
  background: #fff;
  border: 2px solid #f0cbd3;
  box-shadow: 0 14px 35px rgba(90, 28, 47, .08);
  font-size: 26px;
  font-weight: 800;
  color: #7f1c39;
}
.flow {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 22px;
  margin-top: 78px;
}
.node {
  min-width: 230px;
  min-height: 150px;
  padding: 28px 24px;
  border-radius: 34px;
  background: #fff;
  border: 3px solid #efc7d0;
  box-shadow: 0 22px 50px rgba(88, 30, 47, .1);
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 34px;
  line-height: 1.25;
  font-weight: 800;
}
.node.dark {
  color: #fff;
  background: linear-gradient(135deg, #8b1736, #d85e75);
  border: 0;
}
.arrow {
  font-size: 62px;
  color: #b52d4c;
  font-weight: 800;
}
.mini {
  display: block;
  margin-top: 8px;
  font-size: 21px;
  font-weight: 700;
  color: #9b7480;
}
.node.dark .mini { color: #ffe2e8; }
.grid2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 42px;
  margin-top: 70px;
}
.panel {
  min-height: 520px;
  padding: 44px;
  border-radius: 36px;
  background: rgba(255,255,255,.82);
  border: 3px solid #efcbd3;
  box-shadow: 0 24px 70px rgba(88, 30, 47, .10);
}
.panel h2 {
  margin: 0 0 30px;
  font-size: 46px;
  color: #541726;
}
.big-number {
  font-size: 118px;
  font-weight: 800;
  color: #9f1735;
  line-height: 1;
}
.formula {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 118px;
  padding: 20px 42px;
  border-radius: 30px;
  background: #fff;
  border: 3px solid #edc6cf;
  font-size: 44px;
  font-weight: 800;
  color: #521827;
  box-shadow: 0 18px 46px rgba(88, 30, 47, .09);
}
.matrix {
  display: grid;
  grid-template-columns: repeat(8, 58px);
  gap: 10px;
  margin-top: 30px;
}
.cell {
  width: 58px;
  height: 58px;
  border-radius: 14px;
  background: #f7dbe2;
}
.cell.hot { background: #9f1735; }
.cell.mid { background: #d75f74; }
.cell.low { background: #f1b7c3; }
.vector-area {
  position: relative;
  height: 520px;
  margin-top: 52px;
}
.axis {
  position: absolute;
  left: 130px;
  bottom: 68px;
  width: 560px;
  height: 4px;
  background: #d7a4af;
}
.axis.y {
  width: 4px;
  height: 430px;
}
.vec {
  position: absolute;
  left: 130px;
  bottom: 68px;
  width: 500px;
  height: 9px;
  background: #8b1736;
  border-radius: 999px;
  transform-origin: 0 50%;
}
.vec::after {
  content: "";
  position: absolute;
  right: -14px;
  top: -11px;
  border-left: 26px solid #8b1736;
  border-top: 15px solid transparent;
  border-bottom: 15px solid transparent;
}
.vec.b { background: #d86b3d; transform: rotate(-28deg); }
.vec.b::after { border-left-color: #d86b3d; }
.vec.c { background: #d7a4af; transform: rotate(-76deg); width: 420px; }
.vec.c::after { border-left-color: #d7a4af; }
.angle-label {
  position: absolute;
  left: 310px;
  bottom: 155px;
  padding: 12px 20px;
  border-radius: 18px;
  background: #fff;
  font-size: 30px;
  font-weight: 800;
  color: #8b1736;
}
.split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 38px;
  margin-top: 56px;
}
.mode-card {
  min-height: 500px;
  border-radius: 40px;
  padding: 46px;
  background: #fff;
  border: 3px solid #efcbd3;
  box-shadow: 0 24px 70px rgba(88, 30, 47, .1);
}
.mode-card h2 { margin: 0 0 34px; font-size: 52px; color: #541726; }
.result-pill {
  margin-top: 34px;
  padding: 28px 34px;
  border-radius: 28px;
  color: #fff;
  background: linear-gradient(135deg, #8b1736, #d85e75);
  font-size: 38px;
  font-weight: 800;
  text-align: center;
}
.tokens { display: flex; flex-wrap: wrap; gap: 16px; margin-top: 58px; }
.token {
  padding: 18px 24px;
  border-radius: 22px;
  background: #fff;
  border: 3px solid #efcbd3;
  font-size: 34px;
  font-weight: 800;
  color: #541726;
}
.token.dim { opacity: .38; text-decoration: line-through; }
.weights {
  display: flex;
  align-items: flex-end;
  gap: 24px;
  height: 360px;
  margin-top: 46px;
}
.bar {
  width: 118px;
  border-radius: 24px 24px 10px 10px;
  background: linear-gradient(180deg, #8b1736, #e06c82);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 18px;
  color: #fff;
  font-size: 24px;
  font-weight: 800;
}
.bar.lowbar { height: 95px; background: #e7c4cc; color: #734553; }
.bar.midbar { height: 210px; }
.bar.highbar { height: 330px; }
.caption {
  position: absolute;
  left: 98px;
  bottom: 74px;
  font-size: 24px;
  color: #876672;
}
"""


SLIDES = [
    (
        "01_konlpy_okt_concept.png",
        """
        <div class="slide">
          <div class="kicker">STEP 1</div>
          <h1>KoNLPy Okt</h1>
          <div class="subtitle">한국어 문장을 의미 토큰으로 분해</div>
          <div class="tokens">
            <div class="token">건성</div><div class="token">피부</div>
            <div class="token dim">에</div><div class="token">좋다</div>
            <div class="token">수분크림</div><div class="token">추천</div>
            <div class="token">해주다</div><div class="token dim">향</div>
          </div>
          <div class="chip-row">
            <div class="chip">POS Tagging</div><div class="chip">Stemming</div><div class="chip">Stopwords</div>
          </div>
          <div class="brand">MIMO AI RECOMMENDATION PIPELINE</div>
        </div>
        """,
    ),
    (
        "02_konlpy_okt_pipeline.png",
        """
        <div class="slide">
          <div class="kicker">STEP 1 OUTPUT</div>
          <h1>문장 → Clean Text</h1>
          <div class="flow">
            <div class="node dark">입력<br><span class="mini">자유 문장</span></div>
            <div class="arrow">→</div>
            <div class="node">한글<br>필터</div>
            <div class="arrow">→</div>
            <div class="node">Okt.pos</div>
            <div class="arrow">→</div>
            <div class="node">품사<br>필터</div>
            <div class="arrow">→</div>
            <div class="node dark">TF-IDF<br><span class="mini">입력</span></div>
          </div>
          <div class="formula" style="margin-top:86px;">건성 피부 좋다 수분크림 추천 해주다 별로 좋다</div>
          <div class="caption">Noun · Verb · Adjective · length &gt; 1</div>
          <div class="brand">MIMO AI RECOMMENDATION PIPELINE</div>
        </div>
        """,
    ),
    (
        "03_tfidf_concept.png",
        """
        <div class="slide">
          <div class="kicker">STEP 2</div>
          <h1>TF-IDF</h1>
          <div class="subtitle">흔한 단어는 작게, 특징 단어는 크게</div>
          <div class="grid2">
            <div class="panel">
              <h2>Common</h2>
              <div class="weights">
                <div class="bar lowbar">피부</div>
                <div class="bar lowbar">고민</div>
                <div class="bar lowbar">사용</div>
              </div>
            </div>
            <div class="panel">
              <h2>Specific</h2>
              <div class="weights">
                <div class="bar highbar">세라마이드</div>
                <div class="bar midbar">수분크림</div>
                <div class="bar highbar">트러블</div>
              </div>
            </div>
          </div>
          <div class="brand">MIMO AI RECOMMENDATION PIPELINE</div>
        </div>
        """,
    ),
    (
        "04_tfidf_vectorization.png",
        """
        <div class="slide">
          <div class="kicker">STEP 2 MATRIX</div>
          <h1>9031 × 2473</h1>
          <div class="subtitle">상담 질문을 희소 벡터 행렬로 저장</div>
          <div class="grid2">
            <div class="panel">
              <h2>Data</h2>
              <div class="big-number">9031</div>
              <div class="chip-row"><div class="chip">cleaned_question</div></div>
            </div>
            <div class="panel">
              <h2>Vector Space</h2>
              <div class="matrix">
                <div class="cell hot"></div><div class="cell low"></div><div class="cell"></div><div class="cell mid"></div><div class="cell"></div><div class="cell hot"></div><div class="cell low"></div><div class="cell"></div>
                <div class="cell"></div><div class="cell hot"></div><div class="cell mid"></div><div class="cell"></div><div class="cell low"></div><div class="cell"></div><div class="cell hot"></div><div class="cell low"></div>
                <div class="cell low"></div><div class="cell"></div><div class="cell hot"></div><div class="cell low"></div><div class="cell"></div><div class="cell mid"></div><div class="cell"></div><div class="cell hot"></div>
                <div class="cell"></div><div class="cell mid"></div><div class="cell"></div><div class="cell hot"></div><div class="cell low"></div><div class="cell"></div><div class="cell mid"></div><div class="cell"></div>
              </div>
              <div class="chip-row"><div class="chip">tfidf_rebuild.pkl</div><div class="chip">.mtx</div></div>
            </div>
          </div>
          <div class="brand">MIMO AI RECOMMENDATION PIPELINE</div>
        </div>
        """,
    ),
    (
        "05_cosine_concept.png",
        """
        <div class="slide">
          <div class="kicker">STEP 3</div>
          <h1>Cosine Similarity</h1>
          <div class="subtitle">벡터의 크기보다 방향을 비교</div>
          <div class="vector-area">
            <div class="axis"></div><div class="axis y"></div>
            <div class="vec"></div><div class="vec b"></div><div class="vec c"></div>
            <div class="angle-label">작은 각도 = 높은 유사도</div>
          </div>
          <div class="formula">cos(θ) = A · B / ||A||||B||</div>
          <div class="brand">MIMO AI RECOMMENDATION PIPELINE</div>
        </div>
        """,
    ),
    (
        "06_cosine_recommendation.png",
        """
        <div class="slide">
          <div class="kicker">FINAL SCORING</div>
          <h1>추천 계산</h1>
          <div class="split">
            <div class="mode-card">
              <h2>Expert</h2>
              <div class="flow" style="margin-top:20px; gap:14px;">
                <div class="node">cosine</div><div class="arrow">+</div><div class="node">profile<br>bonus</div>
              </div>
              <div class="result-pill">상담 1개 선택</div>
            </div>
            <div class="mode-card">
              <h2>Review</h2>
              <div class="flow" style="margin-top:20px; gap:14px;">
                <div class="node">cosine</div><div class="arrow">→</div><div class="node">dedupe</div>
              </div>
              <div class="result-pill">제품 3개 추천</div>
            </div>
          </div>
          <div class="brand">MIMO AI RECOMMENDATION PIPELINE</div>
        </div>
        """,
    ),
]


def render_html(body):
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width={WIDTH}, height={HEIGHT}">
<style>{STYLE}</style>
</head>
<body>{body}</body>
</html>"""


def main():
    OUT_DIR.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        for name, body in SLIDES:
            html_path = tmp / f"{Path(name).stem}.html"
            png_path = OUT_DIR / name
            html_path.write_text(render_html(body), encoding="utf-8")
            subprocess.run(
                [
                    CHROME,
                    "--headless=new",
                    "--no-sandbox",
                    "--disable-gpu",
                    f"--window-size={WIDTH},{HEIGHT}",
                    f"--screenshot={png_path}",
                    html_path.as_uri(),
                ],
                check=True,
            )
            print(png_path)


if __name__ == "__main__":
    main()
