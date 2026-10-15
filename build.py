"""Builds the static site from content.py.

    python build.py

Writes index.html, work/, about/, contact/ and 404.html next to this file.
Every page holds the English text plus the 中文 text in data-zh attributes;
assets/js/main.js swaps them when the language toggle is pressed.
"""

from html import escape
from pathlib import Path
from urllib.parse import urlparse, quote

from content import SITE, IDENTITY, PROJECTS, ABOUT, T

ROOT = Path(__file__).parent
VERSION = "4"  # bump to bust browser caches of css/js

UI = {
    "work": T("Work", "作品"),
    "about": T("About", "關於"),
    "contact": T("Contact", "聯絡"),
    "menu": T("Menu", "選單"),
    "close": T("Close", "關閉"),
    "navigation": T("Navigation", "導覽"),
    "home": T("Home", "首頁"),
    "built_by": T("Built by", "Built by"),
    "about_me": T("About me", "關於我"),
    "recent_work": T("Recent work", "近期作品"),
    "more_work": T("More work", "更多作品"),
    "view": T("View", "查看"),
    "lets_work": T("Let's work", "一起"),
    "together": T("together", "合作吧"),
    "get_in_touch": T("Get in touch", "與我聯絡"),
    "contact_form": T("Contact form", "聯絡表單"),
    "version": T("Version", "版本"),
    "edition": T("Edition", "版"),
    "local_time": T("Local time", "當地時間"),
    "socials": T("Socials", "社群"),
    "work_title": T("Building sensors and the tools around them", "打造感測器，以及圍繞它們的工具"),
    "all": T("All", "全部"),
    "research": T("Research", "研究"),
    "software": T("Software", "軟體"),
    "project": T("Project", "作品"),
    "category": T("Category", "類別"),
    "year": T("Year", "年份"),
    "role": T("Role", "角色"),
    "status": T("Status", "狀態"),
    "overview": T("Overview", "概述"),
    "what_i_did": T("What I did", "我做了什麼"),
    "tools": T("Tools & methods", "工具與方法"),
    "next_project": T("Next project", "下一個作品"),
    "list_view": T("List view", "列表檢視"),
    "grid_view": T("Grid view", "格狀檢視"),
    "i_can_help": T("What I work with", "我的專長"),
    "education": T("Education", "學歷"),
    "experience": T("Experience", "經歷"),
    "interests": T("Interests", "興趣"),
    "languages": T("Languages", "語言能力"),
    "resume": T("Download résumé", "下載履歷"),
    "contact_title_1": T("Let's start a", "一起開始"),
    "contact_title_2": T("project together", "新的合作"),
    "q_name": T("What's your name?", "您的名字是？"),
    "q_email": T("What's your email?", "您的電子郵件？"),
    "q_org": T("What's the name of your organization?", "您所屬的單位或公司？"),
    "q_topic": T("What is it about?", "想聊什麼？"),
    "q_message": T("Your message", "您的訊息"),
    "ph_name": T("Jane Chen *", "王小明 *"),
    "ph_email": T("jane@example.com *", "name@example.com *"),
    "ph_org": T("University, lab or company", "大學、實驗室或公司"),
    "ph_topic": T("Research collaboration, internship, a role …", "研究合作、實習、職缺……"),
    "ph_message": T("Hello Pavan, can you help me with … *", "Pavan 您好，想請教您關於…… *"),
    "send": T("Send it!", "送出！"),
    "send_note": T("This opens your email app with the message filled in.", "按下後會開啟您的電子郵件程式，並自動填好內容。"),
    "no_email": T("Email address coming soon. Please reach me on GitHub for now.", "電子郵件即將公布，目前請先透過 GitHub 聯絡我。"),
    "contact_details": T("Contact details", "聯絡方式"),
    "location": T("Location", "所在地"),
    "not_found": T("Page not found", "找不到這個頁面"),
    "go_home": T("Back home", "回到首頁"),
    "skip": T("Skip to content", "跳到主要內容"),
    "lang": T("Language", "語言"),
    "open_menu": T("Open menu", "開啟選單"),
    "in_numbers": T("In numbers", "數字看我"),
    "resume_short": T("Résumé", "履歷"),
    "copy_email": T("Copy email", "複製電子郵件"),
    "copied": T("Copied!", "已複製！"),
}


# ---------- helpers ----------

def e(s):
    return escape(s, quote=False)


def a(s):
    return escape(s, quote=True)


def zh(pair):
    """data-zh attribute for a T() pair (empty when both languages match)."""
    if pair["zh"] and pair["zh"] != pair["en"]:
        return f' data-zh="{a(pair["zh"])}"'
    return ""


def t(pair, tag="span", cls="", extra=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c}{zh(pair)}{extra}>{e(pair["en"])}</{tag}>'


def has(pair):
    return bool(pair and pair["en"])


def socials():
    out = []
    if SITE["github"]:
        out.append(("GitHub", SITE["github"]))
    if SITE["linkedin"]:
        out.append(("LinkedIn", SITE["linkedin"]))
    if SITE["email"]:
        out.append(("Email", "mailto:" + SITE["email"]))
    return out


def ext(url):
    return "" if url.startswith("mailto:") else ' target="_blank" rel="noopener noreferrer"'


def btn(href, label, variant="round", extra=""):
    return (
        f'<div class="magnetic"><a class="btn btn--{variant}" href="{a(href)}"{extra}>'
        f'<span class="btn__label">{label}</span><span class="btn__fill" aria-hidden="true"></span></a></div>'
    )


ARROW_DOWN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M5 5l14 14M19 8v11H8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW_UP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M5 19L19 5M8 5h11v11" stroke-linecap="round" stroke-linejoin="round"/></svg>'
GLOBE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><ellipse cx="12" cy="12" rx="4.2" ry="10"/><path d="M2 12h20M3.5 7h17M3.5 17h17"/></svg>'


def open_badge(cls=""):
    if not has(IDENTITY.get("open_to")):
        return ""
    return f'<p class="open {cls}"><span class="open__dot" aria-hidden="true"></span>{t(IDENTITY["open_to"])}</p>'


def portrait(p):
    return p + (SITE["portrait"] or "assets/img/portrait-placeholder.svg")


def avatar(p):
    return p + (SITE["portrait_circle"] or SITE["portrait"] or "assets/img/avatar-placeholder.svg")


def cover(p, proj):
    return f'{p}assets/img/projects/{proj["slug"]}/cover.svg'


def detail(p, proj):
    return f'{p}assets/img/projects/{proj["slug"]}/detail.svg'


# ---------- layout ----------

def header(p, active, light):
    nav = ""
    for key, href in (("work", "work/"), ("about", "about/"), ("contact", "contact/")):
        cur = ' aria-current="page"' if active == key else ""
        nav += f'<li><div class="magnetic"><a class="nav__link" href="{p}{href}"{cur}>{t(UI[key])}<span class="nav__dot" aria-hidden="true"></span></a></div></li>'
    lang = (
        f'<div class="lang" role="group" aria-label="Language">'
        f'<button type="button" data-lang-btn="en" aria-pressed="true">EN</button><span aria-hidden="true"> / </span>'
        f'<button type="button" data-lang-btn="zh" aria-pressed="false">中文</button></div>'
    )
    return f"""
<a class="skip" href="#main">{t(UI["skip"])}</a>
<header class="header{' header--light' if light else ''}">
  <div class="magnetic"><a class="logo" href="{p}" aria-label="{a(SITE["name"])}, home">
    <span class="logo__c" aria-hidden="true">©</span>
    <span class="logo__text"><span class="logo__by">{t(UI["built_by"])}&nbsp;</span><span class="logo__name">{e(SITE["short"])}</span><span class="logo__last">&nbsp;{e(SITE["name"].split(" ", 1)[1])}</span></span>
  </a></div>
  <nav class="nav" aria-label="Primary"><ul>{nav}<li>{lang}</li></ul></nav>
  <div class="header__mobile">{lang}<button type="button" class="header__menu" data-menu-open aria-controls="site-menu" aria-expanded="false"><span class="nav__dot nav__dot--on" aria-hidden="true"></span>{t(UI["menu"])}</button></div>
</header>
<div class="burger-wrap" data-burger><div class="magnetic"><button type="button" class="burger" data-menu-open aria-controls="site-menu" aria-expanded="false" aria-label="{a(UI["open_menu"]["en"])}"><span class="burger__bars" aria-hidden="true"><span></span><span></span></span><span class="btn__fill" aria-hidden="true"></span></button></div></div>
<div class="menu-shade" data-menu-close></div>
<aside class="menu" id="site-menu" aria-label="Menu" hidden>
  <div class="menu__inner">
    <p class="label">{t(UI["navigation"])}</p>
    <ul class="menu__links">
      <li><a href="{p}"{' aria-current="page"' if active == "home" else ""}>{t(UI["home"])}</a></li>
      <li><a href="{p}work/"{' aria-current="page"' if active == "work" else ""}>{t(UI["work"])}</a></li>
      <li><a href="{p}about/"{' aria-current="page"' if active == "about" else ""}>{t(UI["about"])}</a></li>
      <li><a href="{p}contact/"{' aria-current="page"' if active == "contact" else ""}>{t(UI["contact"])}</a></li>
    </ul>
    <div class="menu__foot">
      <p class="label">{t(UI["socials"])}</p>
      <ul class="menu__socials">{"".join(f'<li><a href="{a(u)}"{ext(u)}>{n}</a></li>' for n, u in socials())}{f'<li><a href="{p}{a(SITE["resume"])}" download>{t(UI["resume_short"])}</a></li>' if SITE["resume"] else ""}</ul>
    </div>
  </div>
</aside>"""


def footer(p):
    social_btns = btn(f"{p}contact/", t(UI["contact_form"]), "outline-light")
    if SITE["email"]:
        social_btns = btn("mailto:" + SITE["email"], e(SITE["email"]), "outline-light") + social_btns
    social_btns += btn(SITE["github"], "GitHub", "outline-light", ext(SITE["github"]))
    links = "".join(f'<li><div class="magnetic"><a href="{a(u)}"{ext(u)}>{n}</a></div></li>' for n, u in socials())
    if SITE["resume"]:
        links += f'<li><div class="magnetic"><a href="{p}{a(SITE["resume"])}" download>{t(UI["resume_short"])}</a></div></li>'
    return f"""
<footer class="footer">
  <div class="footer__cap" aria-hidden="true"><div class="footer__capShape" data-cap></div></div>
  <div class="footer__body">
    <h2 class="footer__title">
      <span class="footer__line"><span class="footer__avatar"><img src="{avatar(p)}" alt="" width="100" height="100" loading="lazy"></span>{t(UI["lets_work"])}</span>
      <span class="footer__line">{t(UI["together"])}<span class="footer__arrow">{ARROW_UP}</span></span>
    </h2>
    <div class="footer__divider"><div class="footer__cta" data-parallax="-0.12">{btn(p + "contact/", t(UI["get_in_touch"]), "round-accent")}</div></div>
    <div class="footer__contact">{social_btns}</div>
    <div class="footer__info">
      <div class="footer__group">
        <div><span class="label">{t(UI["version"])}</span><p>{SITE["edition"]} © {t(UI["edition"])}</p></div>
        <div><span class="label">{t(UI["local_time"])}</span><p><time data-clock>--:--</time> GMT+8</p></div>
      </div>
      <div class="footer__socials"><span class="label">{t(UI["socials"])}</span><ul>{links}</ul></div>
    </div>
  </div>
</footer>"""


def page(path, title, desc, body, active=None, light=False, base=None, title_zh=None):
    depth = path.count("/")
    p = "" if base else "../" * depth
    url = SITE["url"] + path
    og_img = SITE["url"] + "assets/img/og.png"
    base_tag = f'<base href="{a(base)}">' if base else ""
    html = f"""<!doctype html>
<html lang="en" data-title-zh="{a(title_zh or title)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{base_tag}
<title>{e(title)}</title>
<meta name="description" content="{a(desc)}">
<link rel="canonical" href="{a(url)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{a(SITE["name"])}">
<meta property="og:title" content="{a(title)}">
<meta property="og:description" content="{a(desc)}">
<meta property="og:url" content="{a(url)}">
<meta property="og:image" content="{a(og_img)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta property="og:locale:alternate" content="zh_TW">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{a(title)}">
<meta name="twitter:description" content="{a(desc)}">
<meta name="twitter:image" content="{a(og_img)}">
<meta name="theme-color" content="#1c1d20">
<link rel="icon" href="{p}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Inter+Tight:wght@400;500&family=Noto+Sans+TC:wght@400;500&display=swap">
<link rel="stylesheet" href="{p}assets/css/style.css?v={VERSION}">
<script>(function(d){{d.classList.add("js");try{{if(localStorage.getItem("lang")==="zh")d.lang="zh-Hant";if(!sessionStorage.getItem("seen-hello")&&!matchMedia("(prefers-reduced-motion: reduce)").matches)d.classList.add("hello")}}catch(e){{}}}})(document.documentElement)</script>
<script src="{p}assets/js/main.js?v={VERSION}" defer></script>
</head>
<body>
<div class="preloader" aria-hidden="true" data-preloader><p class="preloader__word"><span class="preloader__dot"></span><span data-preloader-word>Hello</span></p><svg class="preloader__curve" viewBox="0 0 1000 300" preserveAspectRatio="none"><path d="M0 0 Q500 300 1000 0 Z"/></svg></div>
<div class="cursor" aria-hidden="true" data-cursor><span>{t(UI["view"])}</span></div>
{header(p, active, light)}
<main id="main">
{body}
</main>
{footer(p)}
</body>
</html>
"""
    out = ROOT / (path + "index.html" if path.endswith("/") or path == "" else path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print("wrote", out.relative_to(ROOT))


# ---------- sections ----------

def preview_modal(p):
    slides = "".join(
        f'<div class="preview__slide" style="background:{pr["color"]}"><img src="{cover(p, pr)}" alt="" width="400" height="300" loading="lazy"></div>'
        for pr in PROJECTS
    )
    return f'<div class="preview" aria-hidden="true" data-preview><div class="preview__slider" data-preview-slider>{slides}</div></div>'


def work_rows(p, projects, numbered=True):
    rows = ""
    for i, pr in enumerate(projects):
        href = f"{p}work/{pr['slug']}/"
        sub = f' <span class="row__sub">{t(pr["subtitle"])}</span>' if has(pr["subtitle"]) else ""
        rows += f"""
<div class="row reveal" data-group="{pr['group']}" data-index="{PROJECTS.index(pr)}">
  <a class="row__link" href="{href}" data-preview-index="{PROJECTS.index(pr)}">
    <h3 class="row__title">{t(pr["title"])}{sub}</h3>
    <p class="row__meta">{t(pr["category"])}</p>
    <p class="row__year">{pr["year"]}</p>
  </a>
  <a class="card" href="{href}">
    <span class="card__image" style="background:{pr['color']}"><img src="{cover(p, pr)}" alt="{a(pr['title']['en'])}" width="1200" height="900" loading="lazy"></span>
    <span class="card__title">{f'<span class="card__index">{i + 1:02d}</span>' if numbered else ""}{t(pr["title"])}</span>
    <span class="card__meta">{t(pr["category"])}<span>{pr["year"]}</span></span>
  </a>
</div>"""
    return rows


def build_home():
    p = ""
    name_unit = f'<span class="hero__unit">{e(SITE["name"])}<span class="hero__dash"> — </span></span>'
    copy = f'<div class="marquee__copy">{name_unit * 4}</div>'
    words = IDENTITY["tagline"]
    tiles1 = "".join(f'<div class="gallery__tile" style="background:{pr["color"]}"><img src="{cover(p, pr)}" alt="" loading="lazy"></div>' for pr in PROJECTS)
    order2 = [PROJECTS[i % len(PROJECTS)] for i in (2, 3, 0, 1)]
    tiles2 = "".join(f'<div class="gallery__tile" style="background:{pr["color"]}"><img src="{detail(p, pr)}" alt="" loading="lazy"></div>' for pr in order2)
    body = f"""
<section class="hero" aria-label="Introduction">
  <h1 class="sr-only">{e(SITE["name"])} — {t(IDENTITY["title"])}, {t(IDENTITY["degree"])}. {t(IDENTITY["based"])} {t(IDENTITY["country"])}</h1>
  <div class="hero__portrait"><img src="{portrait(p)}" alt="Portrait of {a(SITE['name'])}" width="887" height="1200" fetchpriority="high"></div>
  <div class="hero__badgeWrap"><div class="magnetic"><div class="hero__badge">
    <p class="hero__badgeText" aria-hidden="true">{t(IDENTITY["based"])}<br>{t(IDENTITY["country"])}</p>
    <span class="hero__globe" aria-hidden="true"><span class="hero__globeDisc">{GLOBE}</span></span>
  </div></div></div>
  <div class="hero__role">
    <span class="hero__arrow">{ARROW_DOWN}</span>
    <p class="hero__roleText">{"".join(t(l, "span", "hero__roleLine") for l in IDENTITY["title_lines"])}<span class="hero__degree">{t(IDENTITY["degree"])}</span></p>
    {open_badge("open--hero")}
  </div>
  {open_badge("open--hero open--heroMobile")}
  <div class="hero__name" aria-hidden="true"><div class="marquee" data-marquee>{copy}{copy}</div></div>
</section>

<section class="intro" aria-label="About in short">
  <div class="intro__body">
    <p class="intro__statement reveal-words"{zh(words)}>{e(words["en"])}</p>
    <div class="intro__side">
      <p class="intro__support reveal"{zh(IDENTITY["intro"])}>{e(IDENTITY["intro"]["en"])}</p>
      <div class="intro__btn" data-parallax="0.1">{btn(p + "about/", t(UI["about_me"]), "round")}</div>
    </div>
  </div>
</section>

<section class="recent" aria-labelledby="recent-heading">
  <div class="recent__inner">
    <h2 class="label recent__heading reveal" id="recent-heading">{t(UI["recent_work"])}</h2>
    <div class="rows">{work_rows(p, PROJECTS)}</div>
    <div class="recent__more reveal">{btn(p + "work/", t(UI["more_work"]) + f'<sup>{len(PROJECTS)}</sup>', "outline")}</div>
  </div>
  {preview_modal(p)}
</section>

<section class="gallery" aria-hidden="true">
  <div class="gallery__row" data-slide="-1">{tiles1}</div>
  <div class="gallery__row" data-slide="1">{tiles2}</div>
</section>
"""
    page("", f'{SITE["name"]} — {IDENTITY["title"]["en"]}', IDENTITY["tagline"]["en"], body, "home", light=True,
         title_zh=f'{SITE["name"]} — {IDENTITY["title"]["zh"]}')


def build_work():
    p = "../"
    counts = {g: sum(1 for pr in PROJECTS if pr["group"] == g) for g in ("research", "software")}
    chips = f'<button type="button" class="chip" data-filter="all" aria-pressed="true">{t(UI["all"])}<sup>{len(PROJECTS)}</sup></button>'
    for g in ("research", "software"):
        chips += f'<button type="button" class="chip" data-filter="{g}" aria-pressed="false">{t(UI[g])}<sup>{counts[g]}</sup></button>'
    body = f"""
<section class="page-head">
  <h1 class="page-title reveal"{zh(UI["work_title"])}>{e(UI["work_title"]["en"])}</h1>
</section>
<section class="work" data-work>
  <div class="work__bar">
    <div class="chips" role="group" aria-label="Filter">{chips}</div>
    <div class="views" role="group" aria-label="View">
      <button type="button" class="view-btn" data-view="list" aria-pressed="true" aria-label="{a(UI['list_view']['en'])}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
      <button type="button" class="view-btn" data-view="grid" aria-pressed="false" aria-label="{a(UI['grid_view']['en'])}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="4" y="4" width="6.5" height="6.5"/><rect x="13.5" y="4" width="6.5" height="6.5"/><rect x="4" y="13.5" width="6.5" height="6.5"/><rect x="13.5" y="13.5" width="6.5" height="6.5"/></svg></button>
    </div>
  </div>
  <div class="work__heads" aria-hidden="true"><span class="label">{t(UI["project"])}</span><span class="label">{t(UI["category"])}</span><span class="label">{t(UI["year"])}</span></div>
  <div class="rows rows--work" data-rows>{work_rows(p, PROJECTS)}</div>
  {preview_modal(p)}
</section>
"""
    page("work/", f'{UI["work"]["en"]} — {SITE["name"]}', "Research and software projects by " + SITE["name"] + ": fiber-optic hydrogen sensing, thin-film sputtering and the tools that support it.",
         body, "work", title_zh=f'{UI["work"]["zh"]} — {SITE["name"]}')


def build_project(i, pr):
    p = "../../"
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    meta = [("role", pr["role"]), ("category", pr["category"]), ("year", T(pr["year"], pr["year"])), ("status", pr["status"])]
    meta_html = "".join(f'<div class="meta__item"><span class="label">{t(UI[k])}</span><p>{t(v)}</p></div>' for k, v in meta if has(v))
    links = "".join(btn(l["url"], t(l["label"]) + " ↗", "round" if j == 0 else "outline", ext(l["url"])) for j, l in enumerate(pr["links"]))
    highlights = "".join(f'<li class="reveal"><span class="hl__n">{j + 1:02d}</span>{t(h)}</li>' for j, h in enumerate(pr["highlights"]))
    stack = "".join(f"<li>{e(s)}</li>" for s in pr["stack"])
    sub = f'<p class="project__sub reveal">{t(pr["subtitle"])}</p>' if has(pr["subtitle"]) else ""
    body = f"""
<article class="project">
  <header class="page-head project__head">
    <p class="label reveal">{f"{i + 1:02d}"} — {t(pr["category"])}</p>
    <h1 class="page-title reveal"{zh(pr["title"])}>{e(pr["title"]["en"])}</h1>
    {sub}
    <div class="meta reveal">{meta_html}</div>
  </header>
  <div class="project__cover reveal" style="background:{pr['color']}"><img src="{cover(p, pr)}" alt="{a(pr['title']['en'])} cover illustration" width="1200" height="900" fetchpriority="high"></div>
  <section class="project__body">
    <div class="project__col">
      <h2 class="label">{t(UI["overview"])}</h2>
    </div>
    <div class="project__text">
      <p class="project__overview reveal"{zh(pr["overview"])}>{e(pr["overview"]["en"])}</p>
      {f'<div class="project__links reveal">{links}</div>' if links else ""}
    </div>
  </section>
  <section class="project__body">
    <div class="project__col"><h2 class="label">{t(UI["what_i_did"])}</h2></div>
    <ol class="hl">{highlights}</ol>
  </section>
  <div class="project__detail reveal" style="background:{pr['color']}"><img src="{detail(p, pr)}" alt="" width="1200" height="900" loading="lazy"></div>
  <section class="project__body">
    <div class="project__col"><h2 class="label">{t(UI["tools"])}</h2></div>
    <ul class="stack reveal">{stack}</ul>
  </section>
  <a class="next" href="{p}work/{nxt['slug']}/">
    <span class="label">{t(UI["next_project"])}</span>
    <span class="next__title">{t(nxt["title"])}</span>
    <span class="next__image" style="background:{nxt['color']}"><img src="{cover(p, nxt)}" alt="" loading="lazy"></span>
  </a>
</article>
"""
    page(f"work/{pr['slug']}/", f'{pr["title"]["en"]} — {SITE["name"]}', pr["summary"]["en"], body, "work",
         title_zh=f'{pr["title"]["zh"]} — {SITE["name"]}')


def timeline(items):
    out = ""
    for it in items:
        where = t(it["where"], "p", "tl__where") if has(it["where"]) else ""
        when = t(it["when"], "p", "tl__when") if has(it["when"]) else '<p class="tl__when"></p>'
        notes = t(it["notes"], "p", "tl__notes") if has(it.get("notes")) else ""
        out += f'<li class="tl__item reveal"><div>{t(it["what"], "h3", "tl__what")}{where}{notes}</div>{when}</li>'
    return f'<ul class="tl">{out}</ul>'


def build_about():
    p = "../"
    paras = "".join(f'<p class="reveal"{zh(b)}>{e(b["en"])}</p>' for b in ABOUT["body"])
    skills = ""
    for j, s in enumerate(ABOUT["skills"]):
        items = "".join(f"<li>{t(x)}</li>" for x in s["items"])
        skills += f'<div class="skill reveal"><span class="skill__n">{j + 1:02d}</span><h3 class="skill__title">{t(s["title"])}</h3><ul>{items}</ul></div>'
    interests = "".join(f'<li>{t(x)}</li>' for x in ABOUT["interests"])
    languages = "".join(f'<li>{t(x)}</li>' for x in ABOUT.get("languages", []))
    stats = "".join(f'<li class="stat reveal"><span class="stat__value">{e(x["value"])}</span>{t(x["label"], "span", "stat__label")}</li>' for x in ABOUT.get("stats", []))
    resume = f'<div class="about__resume reveal">{btn(p + SITE["resume"], t(UI["resume_short"]) + " ↓", "round", " download")}</div>' if SITE["resume"] else ""
    body = f"""
<section class="page-head">
  <h1 class="page-title page-title--about reveal"{zh(ABOUT["headline"])}>{e(ABOUT["headline"]["en"])}</h1>
</section>
<section class="about">
  <div class="about__divider"><div class="about__globe" data-parallax="-0.08"><span class="hero__globeDisc about__globeDisc">{GLOBE}</span></div></div>
  <div class="about__grid">
    <div class="about__text"><span class="about__arrow">{ARROW_DOWN}</span>{paras}{resume}</div>
    <div class="about__portrait reveal"><img src="{portrait(p)}" alt="Portrait of {a(SITE['name'])}" width="887" height="1200" loading="lazy"></div>
  </div>
</section>
<section class="stats" aria-labelledby="stats-heading">
  <h2 class="label" id="stats-heading">{t(UI["in_numbers"])}</h2>
  <ul class="stats__grid">{stats}</ul>
</section>
<section class="skills">
  <h2 class="section-title reveal">{t(UI["i_can_help"])}</h2>
  <div class="skills__grid">{skills}</div>
</section>
<section class="cv">
  <div class="cv__block"><h2 class="label">{t(UI["education"])}</h2>{timeline(ABOUT["education"])}</div>
  <div class="cv__block"><h2 class="label">{t(UI["experience"])}</h2>{timeline(ABOUT["experience"])}</div>
  <div class="cv__block"><h2 class="label">{t(UI["languages"])}</h2><ul class="stack reveal">{languages}</ul><h2 class="label cv__sub">{t(UI["interests"])}</h2><ul class="stack reveal">{interests}</ul></div>
</section>
"""
    page("about/", f'{UI["about"]["en"]} — {SITE["name"]}', IDENTITY["intro"]["en"], body, "about",
         title_zh=f'{UI["about"]["zh"]} — {SITE["name"]}')


def field(n, q, name, ph, kind="input", required=False):
    req = " required" if required else ""
    ctrl = (
        f'<textarea id="f-{name}" name="{name}" rows="4" placeholder="{a(ph["en"])}" data-zh-placeholder="{a(ph["zh"])}"{req}></textarea>'
        if kind == "textarea"
        else f'<input id="f-{name}" name="{name}" type="{"email" if name == "email" else "text"}" placeholder="{a(ph["en"])}" data-zh-placeholder="{a(ph["zh"])}"{req}>'
    )
    return f'<div class="field"><span class="field__n">{n:02d}</span><label for="f-{name}">{t(q)}</label>{ctrl}</div>'


def build_contact():
    p = "../"
    details = ""
    if SITE["email"]:
        details += f'<li><a href="mailto:{a(SITE["email"])}">{e(SITE["email"])}</a> <button type="button" class="copy" data-copy="{a(SITE["email"])}" data-copied-en="{a(UI["copied"]["en"])}" data-copied-zh="{a(UI["copied"]["zh"])}">{t(UI["copy_email"])}</button></li>'
    if SITE["linkedin"]:
        details += f'<li><a href="{a(SITE["linkedin"])}"{ext(SITE["linkedin"])}>LinkedIn</a></li>'
    details += f'<li><a href="{a(SITE["github"])}"{ext(SITE["github"])}>GitHub</a></li>'
    resume = f'<li><a href="{p}{a(SITE["resume"])}" download>{t(UI["resume"])}</a></li>' if SITE["resume"] else ""
    disabled = "" if SITE["email"] else " disabled"
    note = UI["send_note"] if SITE["email"] else UI["no_email"]
    body = f"""
<section class="contact">
  <div class="contact__head">
    <h1 class="page-title"><span class="contact__avatar"><img src="{avatar(p)}" alt="" width="100" height="100"></span>{t(UI["contact_title_1"], "span", "reveal")}<br>{t(UI["contact_title_2"], "span", "reveal")}</h1>
    {open_badge("open--contact")}
    <span class="contact__arrow">{ARROW_DOWN}</span>
  </div>
  <div class="contact__grid">
    <form class="form" data-contact-form data-email="{a(SITE['email'])}">
      {field(1, UI["q_name"], "name", UI["ph_name"], required=True)}
      {field(2, UI["q_email"], "email", UI["ph_email"], required=True)}
      {field(3, UI["q_org"], "org", UI["ph_org"])}
      {field(4, UI["q_topic"], "topic", UI["ph_topic"])}
      {field(5, UI["q_message"], "message", UI["ph_message"], "textarea", required=True)}
      <div class="form__send"><div class="magnetic"><button type="submit" class="btn btn--round-accent btn--big"{disabled}><span class="btn__label">{t(UI["send"])}</span><span class="btn__fill" aria-hidden="true"></span></button></div></div>
      <p class="form__note">{t(note)}</p>
    </form>
    <aside class="contact__aside">
      <div><h2 class="label">{t(UI["contact_details"])}</h2><ul>{details}{resume}</ul></div>
      <div><h2 class="label">{t(UI["location"])}</h2><ul><li>{t(IDENTITY["location"])}</li><li>GMT+8 · <time data-clock>--:--</time></li></ul></div>
    </aside>
  </div>
</section>
"""
    page("contact/", f'{UI["contact"]["en"]} — {SITE["name"]}', "Get in touch with " + SITE["name"] + " about research collaborations, internships or roles.", body, "contact",
         title_zh=f'{UI["contact"]["zh"]} — {SITE["name"]}')


def build_404():
    base = urlparse(SITE["url"]).path or "/"
    body = f"""
<section class="page-head notfound">
  <p class="label">404</p>
  <h1 class="page-title"{zh(UI["not_found"])}>{e(UI["not_found"]["en"])}</h1>
  {btn("./", t(UI["go_home"]), "round")}
</section>
"""
    page("404.html", f'404 — {SITE["name"]}', "Page not found.", body, base=base, title_zh=f'404 — {SITE["name"]}')


def build_sitemap():
    urls = ["", "work/", "about/", "contact/"] + [f"work/{pr['slug']}/" for pr in PROJECTS]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "".join(f"  <url><loc>{e(SITE['url'] + quote(u))}</loc></url>\n" for u in urls)
    xml += "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}sitemap.xml\n", encoding="utf-8")


if __name__ == "__main__":
    build_home()
    build_work()
    for i, pr in enumerate(PROJECTS):
        build_project(i, pr)
    build_about()
    build_contact()
    build_404()
    build_sitemap()
