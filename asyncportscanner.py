import asyncio #This function is imported to read all the ports asynchronously as the ports are scanned actually fast without any traffic stoppage(literally!!!)
import time #IT'S TIME MAN WHAT ELSE COULD THIS BE FOR...

async def port_scanner(host,port,timeout=0.5): #Calling the port scanning function 
    try: #A method similar to if-else and instead of giving a conditon earlier it takes the code inside of it as a condition
        reader,writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout) #I know I knwo reader is not used anywhere but we use it to actually know if the port is getting the call or not, we can't remove it just like that
        writer.close()
        await writer.wait_closed()
        return port
    except Exception:
       return None
    #I don't think I need to tell about the rest

async def main(host, port_start=1, port_end=8000, concurrency = 100): # function where scanning actually happens...
    start_time = time.perf_counter()
    port = range(port_start, port_end+1)
    sem = asyncio.Semaphore(concurrency)
    async def sem_scan(p):
        async with sem:
            return await port_scanner(host, p)
    task  = [asyncio.create_task(sem_scan(p)) for p in port]
    result = await asyncio.gather(*task)
    elapsed_time = time.perf_counter() - start_time
    return sorted([r for r in result if r is not None]), elapsed_time
    
if __name__ == "__main__":
    host = input("Enter an IpV4 address: ").strip()
    Openports, elapsed_time = asyncio.run(main(host, 1, 8001, concurrency=100))
    print(f"Open Ports: {Openports}\nScan time: {elapsed_time: .2f}s")
