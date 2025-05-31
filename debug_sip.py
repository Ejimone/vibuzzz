import asyncio
import os
from dotenv import load_dotenv
from livekit import api

load_dotenv()

async def list_sip_trunks():
    livekit_api = api.LiveKitAPI(
        url=os.getenv("LIVEKIT_URL"),
        api_key=os.getenv("LIVEKIT_API_KEY"),
        api_secret=os.getenv("LIVEKIT_API_SECRET")
    )
    
    try:
        # List all SIP trunks to see what's available
        trunks = await livekit_api.sip.list_sip_trunk()
        print(f"Available SIP trunks: {trunks}")
        
        for trunk in trunks:
            print(f"Trunk ID: {trunk.sip_trunk_id}")
            
    except Exception as e:
        print(f"Error listing SIP trunks: {e}")
    finally:
        await livekit_api.aclose()

asyncio.run(list_sip_trunks())