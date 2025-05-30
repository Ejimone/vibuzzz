import asyncio
import os
import dotenv
from dotenv import load_dotenv
load_dotenv()

from livekit import api 
from livekit.protocol.sip import CreateSIPParticipantRequest, SIPParticipantInfo



token = token = api.AccessToken(os.getenv('LIVEKIT_API_KEY'), os.getenv('LIVEKIT_API_SECRET')) \
    .with_identity("identity") \
    .with_name("name") \
    .with_grants(api.VideoGrants(
        room_join=True,
        room="my-room",
    )).to_jwt()

async def main():
    livekit_api = api.LiveKitAPI()

    request = CreateSIPParticipantRequest(
        sip_trunk_id = os.getenv("SIP_TRUNK_ID"),
        sip_call_to = os.getenv("CUSTOMER_SERVICE_PHONE_NUMBER"),
        room_name = "my-sip-room",
        participant_identity = "sip-test",
        participant_name = "Test Caller",
        krisp_enabled = True,
        wait_until_answered = True
    )
    
    try:
        participant = await livekit_api.sip.create_sip_participant(request)
        print(f"Successfully created {participant}")
    except Exception as e:
        print(f"Error creating SIP participant: {e}")
    finally:
        await livekit_api.aclose()

asyncio.run(main())