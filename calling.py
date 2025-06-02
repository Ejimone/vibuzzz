import asyncio
import os
import dotenv
from dotenv import load_dotenv
load_dotenv()

from livekit import api 
from livekit.protocol.sip import CreateSIPParticipantRequest, SIPParticipantInfo

# Ensure you have these environment variables set
token = api.AccessToken(os.getenv('LIVEKIT_API_KEY'), os.getenv('LIVEKIT_API_SECRET')) \
    .with_identity("identity") \
    .with_name("name") \
    .with_grants(api.VideoGrants(
        room_join=True,
        room="my-r`oom",
    )).to_jwt()

async def main():
    # Initialize LiveKitAPI with proper configuration
    livekit_api = api.LiveKitAPI(
        url=os.getenv("LIVEKIT_URL"),  # Make sure this is set
        api_key=os.getenv("LIVEKIT_API_KEY"),
        api_secret=os.getenv("LIVEKIT_API_SECRET")
    )

    # Verify environment variables are set
    required_vars = ["SIP_TRUNK_ID", "CUSTOMER_SERVICE_PHONE_NUMBER", "LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Missing required environment variables: {missing_vars}")
        return

    request = CreateSIPParticipantRequest(
        sip_trunk_id=os.getenv("SIP_TRUNK_ID"),
        sip_call_to=os.getenv("CUSTOMER_SERVICE_PHONE_NUMBER"),
        room_name="my-sip-room",
        participant_identity="sip-test",
        participant_name="Test Caller",
        krisp_enabled=True,
        wait_until_answered=True
    )
    
    try:
        # Debug: Print the SIP trunk ID being used
        print(f"Using SIP Trunk ID: {os.getenv('SIP_TRUNK_ID')}")
        
        participant = await livekit_api.sip.create_sip_participant(request)
        print(f"Successfully created {participant}")
    except Exception as e:
        print(f"Error creating SIP participant: {e}")
        print(f"Error type: {type(e)}")
    finally:
        await livekit_api.aclose()

asyncio.run(main())