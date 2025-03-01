import time
from time import sleep

import streamlit as st

from streamlit_extras.stylable_container import stylable_container
import frontmatter

import os


def is_lesson_page(my_path):
    page_num = get_page_num(my_path)
    if page_num < 0:
        return False
    return True


def get_sorted_page_files():
    app_dir = os.path.dirname(os.path.abspath(__file__))
    pages_dir = os.path.join(app_dir, "lesson_pages")

    page_files = []
    for file in os.listdir(pages_dir):
        if file.endswith('.py') and file != '__init__.py' and is_lesson_page(file):
            page_files.append(os.path.relpath(os.path.join(pages_dir, file), app_dir))

    return sorted(page_files)


def get_page_num(page_path):
    file_name = os.path.basename(page_path)
    parts = file_name.split("_")
    try:
        return int(parts[0])
    except ValueError:
        return -1


def my_link_button(label, new_page, page_path):
    with stylable_container(
            key="course-nav-btn",
            css_styles="""
            div.course-nav-btn {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 0.5rem;
            }
            div.course-nav-btn > span {
                
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: 0.5rem;
               
                
            }
            div.course-nav-btn > span > a {
                text-decoration: none;
                color: #000;
            }

            div.course-nav-btn > span > a:hover {
                text-decoration: underline;
            }
            div.next-btn {
                text-align: right;
            }
            """,
    ):
        # align = "next-btn" if "next" in label.lower() else "prev-btn"
        if st.button(label, key=label):
            st.switch_page(page_path)


def setup_sidebar():
    st.sidebar.image("static/thumb_learnedmemory_logo_square.png")
    st.sidebar.title("Study Techniques Course")
    with st.sidebar:
        st.link_button("https://learnedmemory.com", "https://learnedmemory.com")


def get_page_dict():
    pages = get_sorted_page_files()
    page_dict = {}
    for page_num, page_path in enumerate(pages):
        page = st.Page(page_path)
        title = title_for_page(page_path, page.title)
        title = f"Lesson {page_num}: {title}"
        page_dict[title] = (page, page_path)
    return page_dict


def show_toc():
    page_dict = get_page_dict()
    for title, (page, page_path) in page_dict.items():
        with st.container():
            my_link_button(title, page, page_path)


def title_for_page(page_path, default_title=None):
    try:
        content_path = content_path_for_page(page_path)
        if not content_path:
            return default_title
    except FileNotFoundError:
        return default_title
    metadata, content = load_markdown(content_path)
    title = title_from_metadata(metadata, default_title)
    return title


def title_from_metadata(metadata, default_title):
    title = metadata.get("title", default_title)
    return title


def show_page_controls(my_path):
    page_num = get_page_num(my_path)
    pages = get_sorted_page_files()
    col1, col2 = st.columns(2)
    with col1:
        if page_num > 0:
            prev_path = pages[page_num - 1]
            prev_page = st.Page(prev_path)
            prev_title = title_for_page(prev_path, prev_page.title)
            my_link_button(f"Previous: {prev_title}", prev_page, prev_path)
    with col2:
        if page_num < len(pages) - 1:
            next_path = pages[page_num + 1]
            next_page = st.Page(next_path)
            next_title = title_for_page(next_path, next_page.title)
            my_link_button(f"Next: {next_title}", next_page, next_path)


DEFAULT_EXTRAS = [
    'fenced-code-blocks',
    'footnotes',
    'metadata',
    'cuddled-lists',
    'pyshell',
    'smarty-pants',
    'spoiler',
    'tables'
]


def load_markdown(md_path):
    with open(md_path) as md_in:
        metadata, content = frontmatter.parse(md_in.read())

    return metadata, content


def render_content_page(my_path):
    setup_sidebar()
    show_markdown_for_page(my_path)
    show_page_controls(my_path)


def show_markdown_for_page(my_path):
    content_path = content_path_for_page(my_path)
    if content_path:
        metadata, content = load_markdown(content_path)
        page = st.Page(my_path)
        title = title_from_metadata(metadata, page.title)
        st.title(title)

        st.markdown(content)


def content_path_for_page(my_path):
    page_num = get_page_num(my_path)
    if page_num < 0:
        return None
    content_path = f"content/lesson_{page_num}.md"
    return content_path



def setup_navigation():
    page_dict = get_page_dict()
    nav_pages = [p[0] for p in page_dict.values()]
    pg = st.navigation(nav_pages)

    pg.run()  # This runs the page.


def embed_video(video_url):
    st.video(video_url, format="video/mp4")
