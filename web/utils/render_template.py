import jinja2
from info import *
from web.server import Webavbot
from utils import get_size
from web.utils.file_properties import get_file_ids
from web.server.exceptions import InvalidHash
import urllib.parse
import logging
import aiohttp
from pathlib import Path
from Template import jisshu_template

#Dont Remove My Credit @AV_BOTz_UPDATE 
#This Repo Is By @BOT_OWNER26 
# For Any Kind Of Error Ask Us In Support Group @AV_SUPPORT_GROUP

async def render_page(id, secure_hash, src=None):
    file = await Webavbot.get_messages(int(BIN_CHANNEL), int(id))
    file_data = await get_file_ids(Webavbot, int(BIN_CHANNEL), int(id))
    if file_data.unique_id[:6] != secure_hash:
        logging.debug(f"link hash: {secure_hash} - {file_data.unique_id[:6]}")
        logging.debug(f"Invalid hash for message with - ID {id}")
        raise InvalidHash

    src = urllib.parse.urljoin(
        URL,
        f"{id}?hash={secure_hash}",
    )

    tag = file_data.mime_type.split("/")[0].strip()
    file_size = humanbytes(file_data.file_size)

    if tag in ["video", "audio"]:
        template_name = "req.html"
    else:
        template_name = "dl.html"
        async with aiohttp.ClientSession() as s:
            async with s.get(src) as u:
                file_size = humanbytes(int(u.headers.get("Content-Length")))

    # ✅ Use Pathlib to get the correct /template folder
    BASE_DIR = Path(__file__).resolve().parent.parent  # Goes from /util → /Deendayal_botz
    template_path = BASE_DIR / "template"

    # ✅ Load Jinja2 environment
    template_loader = jinja2.FileSystemLoader(searchpath=str(template_path))
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template_name)

    file_name = file_data.file_name.replace("_", " ")

    # ✅ Render HTML with all variables
    return template.render(
        file_name=file_name,
        file_url=src,
        file_size=file_size,
        file_unique_id=file_data.unique_id,
        template_ne=jisshu_template.JISSHU_NAME,
        jisshu_disclaimer=jisshu_template.JISSHU_DISCLAIMER,
        jisshu_report_link=jisshu_template.JISSHU_REPORT_LINK,
        jisshu_colours=jisshu_template.JISSHU_COLOURS
    )
