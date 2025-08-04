from config.vector_store import get_vector_store
from teams.Round_Robin_Team import get_team
import asyncio
from autogen_agentchat.ui import Console
vector_store,client =  get_vector_store()
team_1 = get_team()

async def main():
    try:
        stream = team_1.run_stream(task = 'In the event of delay of the airlines, whilst on a Trip, at any airport specified in the Insured Person’s main trave')
        await Console(stream = stream)

    except Exception as e:
        print(f"Exception occured: {e}\n")
        
    finally:
        await client.close()
        
    
if (__name__ == '__main__'):
    asyncio.run(main())


