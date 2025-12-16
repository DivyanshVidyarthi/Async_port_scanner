import asyncio
import time 

async def port_scanner(host,port,timeout=0.5):
    try:
        reader,writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout)
        writer.close()
        await writer.wait_closed()
        return port
    except Exception:
       return None
    

async def main(host, port_start=1, port_end=8000, concurrency = 100):
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
