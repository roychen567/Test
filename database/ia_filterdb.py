import logging
from struct import pack
import re
import asyncio
import base64
from pyrogram.file_id import FileId
from pymongo.errors import DuplicateKeyError
from umongo import Instance, Document, fields
from motor.motor_asyncio import AsyncIOMotorClient
from marshmallow.exceptions import ValidationError
from info import DATABASE_URI2, DATABASE_NAME, DATABASE_URI, DATABASE_URI3, COLLECTION_NAME, USE_CAPTION_FILTER

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]
instance = Instance.from_db(db)

client2 = AsyncIOMotorClient(DATABASE_URI2)
db2 = client2[DATABASE_NAME]
instance = Instance.from_db(db2)

client3 = AsyncIOMotorClient(DATABASE_URI3)
db3 = client3[DATABASE_NAME]
instance = Instance.from_db(db3)


@instance.register
class Media(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)
    
    class Meta:
        indexes = ('$file_name', )
        collection_name = COLLECTION_NAME

# Create separate instances for each database
instance2 = Instance.from_db(db2)
instance3 = Instance.from_db(db3)

@instance2.register
class Media2(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)
    
    class Meta:
        indexes = ('$file_name', )
        collection_name = COLLECTION_NAME

@instance3.register
class Media3(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)
    
    class Meta:
        indexes = ('$file_name', )
        collection_name = COLLECTION_NAME
        
async def save_file(media):
    """Save file in database"""

    # TODO: Find better way to get same file_id for same media to avoid duplicates
    file_id, file_ref = unpack_new_file_id(media.file_id)
    file_name = re.sub(r"(_|\+\s|\-|\.|\+|\[MM\]\s|\[MM\]_|\@TvSeriesBay|\@Cinema\sCompany|\@Cinema_Company|\@CC_|\@CC|\@MM_New|\@MM_Linkz|\@MOVIEHUNT|\@CL|\@FBM|\@CKMSERIES|www_DVDWap_Com_|MLM|\@WMR|\[CF\]\s|\[CF\]|\@IndianMoviez|\@tamil_mm|\@infotainmentmedia|\@trolldcompany|\@Rarefilms|\@yamandanmovies|\[YM\]|\@Mallu_Movies|\@YTSLT|\@DailyMovieZhunt|\@I_M_D_B|\@CC_All|\@PM_Old|Dvdworld|\[KMH\]|\@FBM_HW|\@Film_Kottaka|\@CC_X265|\@CelluloidCineClub|\@cinemaheist|\@telugu_moviez|\@CR_Rockers|\@CCineClub|KC_|\[KC\])", " ", str(media.file_name))   
    try:
        file = Media(
            file_id=file_id,
            file_ref=file_ref,
            file_name=file_name,
            file_size=media.file_size,
            file_type=media.file_type,
            mime_type=media.mime_type,
            caption=media.caption.html if media.caption else None,
        )
    except ValidationError:
        logger.exception('Error occurred while saving file in database')
        return False, 2
    else:
        try:
            await file.commit()
        except DuplicateKeyError:      
            logger.warning(
                f'{getattr(media, "file_name", "NO_FILE")} is already saved in database'
            )

            return False, 0
        else:
            logger.info(f'{getattr(media, "file_name", "NO_FILE")} is saved to database')
            return True, 1
            
async def get_search_results(query, file_type=None, max_results=8, offset=0, filter=False):
    """For given query return (results, next_offset, total_results)"""

    query = query.strip()

    if not query:
        raw_pattern = '.'
    elif ' ' not in query:
        raw_pattern = r'(?i)(\b|[.\+\-_:]|\s|&)' + re.escape(query) + r'(\b|[.\+\-_:]|\s|&)'
    else:
        # Escape individual parts of the query and join with the wildcard
        escaped_parts = [re.escape(part) for part in query.split()]
        raw_pattern = r'(?i)' + r'.*[&\s\.\+\-_()\[\]:]'.join(escaped_parts)

    try:
        regex = re.compile(raw_pattern)
    except re.error as e:
        print(f"Regex compilation error: {e}, pattern: {raw_pattern}")
        return [], '', 0

    filter_query = {}
    if USE_CAPTION_FILTER:
        filter_query['$or'] = [{'file_name': regex}, {'caption': regex}]
    else:
        filter_query['file_name'] = regex

    if file_type:
        filter_query['file_type'] = file_type

    try:
        files_media = await Media.find(filter_query).sort('$natural', -1).to_list(length=48) # Fetch all matching documents
    except Exception as e:
        print(f"Error during MongoDB query: {e}, query: {filter_query}")
        return [], '', 0

    if offset < 0:
        offset = 0

    total_results = len(files_media)
    files = files_media[offset:offset + max_results]
    next_offset = offset + len(files)

    if next_offset < total_results:
        return files, next_offset, total_results
    else:
        return files, '', total_results
        
async def get_bad_files(query, file_type=None, filter=False):
    """For given query return (results, next_offset)"""
    query = query.strip()

    if not query:
        raw_pattern = '.'
    elif ' ' not in query:
        raw_pattern = r'(\b|[\.\+\-_])' + query + r'(\b|[\.\+\-_])'
    else:
        raw_pattern = query.replace(' ', r'.*[\s\.\+\-_]')

    try:
        regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except:
        return []

    if USE_CAPTION_FILTER:
        filter = {'file_name': regex}
    else:
        filter = {'file_name': regex}

    if file_type:
        filter['file_type'] = file_type

    total_results = await Media.count_documents(filter)
    
    cursor_media1 = Media.find(filter)
    cursor_media1.sort('$natural', -1)
    files_media1 = await cursor_media1.to_list(length=total_results)

    return files_media1, total_results
    
async def get_file_details(query):
    filter = {'file_id': query}
    cursor = Media.find(filter)
    filedetails = await cursor.to_list(length=1)
    if filedetails:
        return filedetails

def encode_file_id(s: bytes) -> str:
    r = b""
    n = 0

    for i in s + bytes([22]) + bytes([4]):
        if i == 0:
            n += 1
        else:
            if n:
                r += b"\x00" + bytes([n])
                n = 0

            r += bytes([i])

    return base64.urlsafe_b64encode(r).decode().rstrip("=")


def encode_file_ref(file_ref: bytes) -> str:
    return base64.urlsafe_b64encode(file_ref).decode().rstrip("=")


def unpack_new_file_id(new_file_id):
    """Return file_id, file_ref"""
    decoded = FileId.decode(new_file_id)
    file_id = encode_file_id(
        pack(
            "<iiqq",
            int(decoded.file_type),
            decoded.dc_id,
            decoded.media_id,
            decoded.access_hash
        )
    )
    file_ref = encode_file_ref(decoded.file_reference)
    return file_id, file_ref

async def get_total_files_count():
    """Get total files count from all three databases"""
    try:
        count1 = await Media.count_documents()
        count2 = await Media2.count_documents()
        count3 = await Media3.count_documents()
        return count1 + count2 + count3
    except Exception as e:
        logger.exception(f"Error counting files: {e}")
        return 0

async def get_individual_db_counts():
    """Get individual file counts from each database"""
    try:
        count1 = await Media.count_documents()
        count2 = await Media2.count_documents()
        count3 = await Media3.count_documents()
        return count1, count2, count3
    except Exception as e:
        logger.exception(f"Error counting individual files: {e}")
        return 0, 0, 0

def get_readable_time(seconds) -> str:
    """
    Return a human-readable time format
    """

    result = ""
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)

    if days != 0:
        result += f"{days}d"
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)

    if hours != 0:
        result += f"{hours}h"
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)

    if minutes != 0:
        result += f"{minutes}m"

    seconds = int(seconds)
    result += f"{seconds}s"
    return result
