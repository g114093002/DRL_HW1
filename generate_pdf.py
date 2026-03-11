import os
import markdown
import asyncio
from playwright.async_api import async_playwright

async def generate_pdf():
    # Read markdown content
    with open('conversation_history.md', 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    # Convert to HTML
    html_body = markdown.markdown(md_text, extensions=['fenced_code', 'tables'])
    
    # Add GitHub-like CSS for better styling and Chinese font support
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Microsoft JhengHei";
                line-height: 1.6;
                color: #24292e;
                max-width: 800px;
                margin: 0 auto;
                padding: 40px;
            }}
            h1, h2, h3 {{ border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }}
            pre {{ background-color: #f6f8fa; padding: 16px; border-radius: 3px; overflow: auto; }}
            code {{ background-color: rgba(27,31,35,0.05); padding: 0.2em 0.4em; border-radius: 3px; font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace; }}
            blockquote {{ margin: 0; padding: 0 1em; color: #6a737d; border-left: 0.25em solid #dfe2e5; }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    
    temp_html = "temp_render.html"
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Use playwright to print to PDF
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # use file:// protocol to load local html
        curr_dir = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')
        await page.goto(f"file:///{curr_dir}/{temp_html}")
        await page.pdf(path="Chat_History.pdf", format="A4", print_background=True, margin={"top":"2cm", "bottom":"2cm", "left":"2cm", "right":"2cm"})
        await browser.close()
        
    os.remove(temp_html)
    print("PDF generated successfully.")

if __name__ == "__main__":
    asyncio.run(generate_pdf())
